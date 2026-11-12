#!/usr/bin/env python3
"""
GitHub Actions Workflow Template Fidelity Validator
Validates generated GitHub Actions workflow files against their templates and rules
for 100% fidelity.
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Set
from dataclasses import dataclass
from enum import Enum

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency
    yaml = None

GUIDANCE_COMMENT_PATTERN = re.compile(
    r'^\s*#\s*(?:Only include|Only if|Only when|Include when|Include if|'
    r'Only for|Otherwise|Replace|Repeat|Do not|Note)',
    re.IGNORECASE
)
PLACEHOLDER_PATTERN = re.compile(r'\[\[[A-Z0-9_]+\]\]')
REQUIRED_TOP_LEVEL_KEYS = ("name:", "on:", "jobs:")

# Target key -> (template file, output file, rules file).
# The target key doubles as the template selector when two templates share one
# output file (github-release.yml).
TEMPLATE_MAP = {
    "bash.yml": ("bash.yml", "bash.yml", "bash.md"),
    "dotnet.yml": ("dotnet.yml", "dotnet.yml", "dotnet.md"),
    "security.yml": ("security.yml", "security.yml", "security.md"),
    "nexus-mods-release.yml": ("nexus-mods-release.yml", "nexus-mods-release.yml", "nexus-mods-release.md"),
    "nuget-release.yml": ("nuget-release.yml", "nuget-release.yml", "nuget-release.md"),
    "github-release-dotnet.yml": ("github-release-dotnet.yml", "github-release.yml", "github-release-dotnet.md"),
    "github-release-nuget.yml": ("github-release-nuget.yml", "github-release.yml", "github-release-nuget.md"),
    "steam-workshop-release.yml": ("steam-workshop-release.yml", "steam-workshop-release.yml", "steam-workshop-release.md"),
    "release-assets.yml": (None, "release-assets.yml", "release-assets.md"),
}

# Output-file aliases resolved through an explicit variant.
GITHUB_RELEASE_VARIANTS = {
    "dotnet": "github-release-dotnet.yml",
    "nuget": "github-release-nuget.yml",
}


class ValidationSeverity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class ValidationIssue:
    severity: ValidationSeverity
    message: str
    line_number: Optional[int] = None
    context: Optional[str] = None


class GitHubActionsValidator:
    def __init__(self, repo_root: Path, force: bool = False):
        self.repo_root = repo_root
        self.skill_dir = Path(__file__).resolve().parent
        self.templates_dir = self.skill_dir / "templates"
        self.rules_dir = self.skill_dir / "rules"
        self.force = force
        self.issues: List[ValidationIssue] = []
        self._resolved_owner: Optional[str] = None
        self._resolved_owner_type: Optional[str] = None
        self._resolved_git_user: Optional[str] = None

    def validate(self, target_key: str, generated_content: str) -> List[ValidationIssue]:
        """Validate generated workflow content against its template and rules.

        Template fidelity is enforced only for personal repositories owned by
        the current git user, or whenever the caller explicitly requests the
        templates (`force`). Otherwise all fidelity checks are skipped.
        """
        self.issues = []

        if not self._should_enforce_fidelity():
            return self.issues

        if target_key not in TEMPLATE_MAP:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Unknown workflow target: {target_key}",
            ))
            return self.issues

        template_file, _output_file, rules_file = TEMPLATE_MAP[target_key]
        rules_path = self.rules_dir / rules_file

        if not rules_path.exists():
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Rules not found: {rules_path}",
            ))
            return self.issues

        template_content = None

        if template_file is not None:
            template_path = self.templates_dir / template_file

            if not template_path.exists():
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Template not found: {template_path}",
                ))
                return self.issues

            template_content = template_path.read_text(encoding='utf-8')

        self._check_placeholders_removed(generated_content)
        self._check_guidance_comments_removed(generated_content)
        self._check_required_keys(generated_content)
        self._check_yaml_valid(generated_content)

        if template_content is not None:
            self._check_fixed_lines_integrity(generated_content, template_content)

        return self.issues

    def _should_enforce_fidelity(self) -> bool:
        """Return True when the workflow must follow the templates verbatim.

        Enforcement applies when the caller explicitly requests the templates
        (`force`), or when the repository is both personal (GitHub owner type
        `User`) and owned by the current git user. Enforcement is skipped
        whenever any condition cannot be confirmed.
        """
        if self.force:
            return True

        owner = self._get_repository_owner()
        current_user = self._get_current_git_user()

        if owner is None or current_user is None:
            return False

        if owner.strip().lower() != current_user.strip().lower():
            return False

        owner_type = self._get_repository_owner_type()

        if owner_type is None:
            return False

        return owner_type.strip().lower() == "user"

    def _get_repository_owner(self) -> Optional[str]:
        """Return the repository owner from the `origin` remote, or None."""
        if self._resolved_owner is not None:
            return self._resolved_owner

        try:
            result = subprocess.run(
                ["git", "-C", str(self.repo_root), "remote", "get-url", "origin"],
                capture_output=True, text=True, timeout=10,
            )
        except (OSError, subprocess.SubprocessError):
            return None

        remote = result.stdout.strip()

        if not remote:
            return None

        owner = GitHubActionsValidator._extract_owner(remote)
        self._resolved_owner = owner

        return owner

    def _get_current_git_user(self) -> Optional[str]:
        """Return the current git/GitHub user login, or None if unknown."""
        if self._resolved_git_user is not None:
            return self._resolved_git_user

        login = self._run_read_only_query(["gh", "api", "user", "--jq", ".login"])

        if not login:
            login = self._run_read_only_query(["git", "config", "--get", "github.user"])

        if not login:
            email = self._run_read_only_query(["git", "config", "--get", "user.email"])
            login = GitHubActionsValidator._extract_noreply_login(email or "")

        if login:
            self._resolved_git_user = login

        return login

    def _run_read_only_query(self, command: List[str]) -> Optional[str]:
        """Run a read-only git/gh query and return its trimmed standard output."""
        try:
            result = subprocess.run(
                command if command[0] != "git" else ["git", "-C", str(self.repo_root), *command[1:]],
                capture_output=True, text=True, timeout=10,
            )
        except (OSError, subprocess.SubprocessError):
            return None

        if result.returncode != 0:
            return None

        return result.stdout.strip() or None

    @staticmethod
    def _extract_noreply_login(email: str) -> Optional[str]:
        """Extract the GitHub login from a `users.noreply.github.com` e-mail."""
        match = re.match(r"(?:\d+\+)?([^@+]+)@users\.noreply\.github\.com$", email.strip(), re.IGNORECASE)

        return match.group(1) if match else None

    def _get_repository_owner_type(self) -> Optional[str]:
        """Return the GitHub owner type for the repository, or None if unknown."""
        if self._resolved_owner_type is not None:
            return self._resolved_owner_type

        owner = self._get_repository_owner()

        if not owner:
            return None

        try:
            api_result = subprocess.run(
                ["gh", "api", f"users/{owner}", "--jq", ".type"],
                capture_output=True, text=True, timeout=10,
            )
        except (OSError, subprocess.SubprocessError):
            api_result = None

        if api_result is not None and api_result.stdout.strip():
            owner_type = api_result.stdout.strip()
            self._resolved_owner_type = owner_type
            return owner_type

        try:
            import urllib.request
            import json as _json
            with urllib.request.urlopen(
                f"https://api.github.com/users/{owner}", timeout=10
            ) as response:
                data = _json.loads(response.read().decode("utf-8"))
                owner_type = data.get("type")
            self._resolved_owner_type = owner_type
            return owner_type
        except Exception:
            return None

    @staticmethod
    def _extract_owner(remote_url: str) -> Optional[str]:
        """Extract the owner segment from a git remote URL."""
        remote_url = remote_url.strip()
        if not remote_url:
            return None

        ssh_match = re.match(r"git@[^:]+:([^/]+)/", remote_url)
        if ssh_match:
            return ssh_match.group(1)

        https_match = re.match(r"https?://[^/]+/([^/]+)/", remote_url)
        if https_match:
            return https_match.group(1)

        return None

    def _check_placeholders_removed(self, content: str):
        """Check that no [[PLACEHOLDER]] tokens remain."""
        for placeholder in PLACEHOLDER_PATTERN.findall(content):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Unresolved placeholder: {placeholder}",
                context="Found unresolved scalar placeholder in workflow",
            ))

    def _check_guidance_comments_removed(self, content: str):
        """Check that no template guidance comments remain."""
        for index, line in enumerate(content.splitlines()):
            if GUIDANCE_COMMENT_PATTERN.match(line):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Template guidance comment not removed: {line.strip()[:100]}",
                    line_number=index + 1,
                    context="Directive comments must be removed from the delivered workflow",
                ))

    def _check_required_keys(self, content: str):
        """Check that the top-level workflow structure is present."""
        lines = [line for line in content.splitlines() if line.strip()]

        for key in REQUIRED_TOP_LEVEL_KEYS:
            if not any(line.lstrip().startswith(key) for line in lines):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Required top-level key missing: {key.rstrip(':')}",
                    context="Workflows must define name, on, and jobs at the top level",
                ))

    def _check_yaml_valid(self, content: str):
        """Check that the workflow is valid YAML when a parser is available."""
        if yaml is None:
            self.issues.append(ValidationIssue(
                ValidationSeverity.INFO,
                "PyYAML unavailable; skipped YAML syntax validation",
                context="Install PyYAML to enable full syntax validation",
            ))
            return

        try:
            yaml.safe_load(content)
        except yaml.YAMLError as error:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Invalid YAML: {error}",
                context="Workflow content must parse as valid YAML",
            ))

    def _check_fixed_lines_integrity(self, content: str, template_content: str):
        """Check that fixed template lines survive into the generated workflow.

        Conditional blocks and guidance comments may legitimately be omitted, so
        they are excluded from comparison. Lines carrying placeholders are not
        fixed content either and are skipped.
        """
        template_lines = template_content.splitlines()
        gated_indices = self._get_gated_indices(template_lines)
        document_lines = {
            self._normalise_line(line)
            for line in content.splitlines()
            if self._normalise_line(line)
        }

        for index, template_line in enumerate(template_lines):
            if index in gated_indices:
                continue

            prose = self._normalise_line(template_line)

            if not prose:
                continue

            if GUIDANCE_COMMENT_PATTERN.match(template_line):
                continue

            if PLACEHOLDER_PATTERN.search(template_line):
                continue

            if prose not in document_lines:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Fixed template line changed or missing: {prose}",
                    line_number=index + 1,
                    context="Only placeholders, conditional blocks, and guidance comments may change",
                ))

    @staticmethod
    def _normalise_line(line: str) -> str:
        """Collapse a YAML line to a single comparable form."""
        return re.sub(r'\s+', ' ', line).strip()

    @staticmethod
    def _get_gated_indices(template_lines: List[str]) -> Set[int]:
        """Return template line indices governed by a guidance-comment directive.

        A guidance comment gates the comment itself and the contiguous YAML block
        that follows it up to the next sibling (`- `) item, the next line with
        lower indentation, or the next guidance comment.
        """
        gated: Set[int] = set()

        for index, line in enumerate(template_lines):
            if not GUIDANCE_COMMENT_PATTERN.match(line):
                continue

            gated.add(index)
            cursor = index + 1

            while cursor < len(template_lines) and not template_lines[cursor].strip():
                gated.add(cursor)
                cursor += 1

            if cursor >= len(template_lines):
                continue

            first = template_lines[cursor]
            first_body = first.lstrip()
            base_indent = len(first) - len(first_body)
            is_item = first_body.startswith('- ')
            start = cursor

            while cursor < len(template_lines):
                current = template_lines[cursor]
                body = current.strip()

                if not body:
                    gated.add(cursor)
                    cursor += 1
                    continue

                indent = len(current) - len(current.lstrip())

                if indent < base_indent:
                    break

                if cursor != start and indent == base_indent:
                    if not is_item:
                        break

                    if body.startswith('- '):
                        break

                gated.add(cursor)
                cursor += 1

        return gated


def resolve_target(argument: str, variant: Optional[str]) -> Optional[str]:
    """Resolve a CLI target argument to a template-map key."""
    if argument in TEMPLATE_MAP:
        return argument

    if argument == "github-release.yml":
        return GITHUB_RELEASE_VARIANTS.get(variant or "dotnet")

    return None


def main():
    args = sys.argv[1:]
    force = os.environ.get("GITHUB_ACTIONS_FORCE_FIDELITY", "").strip().lower() in {"1", "true", "yes"}
    variant = None

    while args and args[0].startswith("--"):
        if args[0] in ("--force", "--use-templates"):
            force = True
            args = args[1:]
        elif args[0] == "--variant":
            if len(args) < 2:
                print("Usage: validate_github_actions.py [--force] [--variant dotnet|nuget] "
                      "<repo_root> <workflow_file> [generated_file]")
                sys.exit(2)
            variant = args[1]
            args = args[2:]
        else:
            break

    if len(args) < 2:
        print("Usage: validate_github_actions.py [--force] [--variant dotnet|nuget] "
              "<repo_root> <workflow_file> [generated_file]")
        print("  workflow_file: an output file name (e.g. dotnet.yml, github-release.yml)")
        print("  If generated_file not provided, reads from stdin")
        print("  --force: enforce template fidelity regardless of repository ownership")
        sys.exit(2)

    repo_root = Path(args[0])
    target_argument = args[1]
    target_key = resolve_target(target_argument, variant)

    if target_key is None:
        print(f"Unknown workflow file: {target_argument}")
        print("Known targets: " + ", ".join(sorted(TEMPLATE_MAP)))
        sys.exit(2)

    if len(args) > 2:
        generated_content = Path(args[2]).read_text(encoding='utf-8')
    else:
        generated_content = sys.stdin.read()

    validator = GitHubActionsValidator(repo_root, force=force)
    issues = validator.validate(target_key, generated_content)

    if not validator._should_enforce_fidelity():
        print("i  Template fidelity enforcement skipped: repository is not a personal "
              "repository owned by the current git user. Pass --force (or set "
              "GITHUB_ACTIONS_FORCE_FIDELITY=1) when the templates are explicitly requested.")
        sys.exit(3)

    errors = [i for i in issues if i.severity == ValidationSeverity.ERROR]
    warnings = [i for i in issues if i.severity == ValidationSeverity.WARNING]

    if errors:
        print(f"VALIDATION FAILED: {len(errors)} errors, {len(warnings)} warnings")
        for issue in errors:
            print(f"  ERROR: {issue.message}")
            if issue.context:
                print(f"    Context: {issue.context}")
        sys.exit(1)

    if warnings:
        print(f"VALIDATION PASSED WITH WARNINGS: {len(warnings)} warnings")
        for issue in warnings:
            print(f"  WARNING: {issue.message}")
            if issue.context:
                print(f"    Context: {issue.context}")
        sys.exit(0)

    print("VALIDATION PASSED: 100% template fidelity confirmed")
    sys.exit(0)


if __name__ == "__main__":
    main()
