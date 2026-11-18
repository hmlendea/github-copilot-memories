#!/usr/bin/env python3
"""
GitHub MD Template Fidelity Validator
Validates generated GitHub markdown files against templates and rules for 100% fidelity.
"""

import collections
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Set
from dataclasses import dataclass
from enum import Enum

CONDITIONAL_DIRECTIVE_PATTERN = re.compile(
    r'^\s*<!--\s*(?:Only if|Only when|Include when|Include if|Only for|Always include)\b[^>]*-->',
    re.IGNORECASE
)
INLINE_CONDITIONAL_PATTERN = re.compile(
    r'<!--\s*(?:Only if|Only when|Include when|Include if|Only for|Always include)\b[^>]*-->',
    re.IGNORECASE
)
PLACEHOLDER_PATTERN = re.compile(r'\[\[\[.*?\]\]\]|\[\[.*?\]\]')
HEADING_PATTERN = re.compile(r'^(#{1,6})\s')
LIST_MARKER_PATTERN = re.compile(r'^(?:[-*+]\s+|\d+[.)]\s+)')


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


class GitHubMDValidator:
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

    def validate(self, target_file: str, generated_content: str) -> List[ValidationIssue]:
        """Validate generated content against template and rules.

        Template fidelity is enforced only for personal repositories owned by
        the current git user, or whenever the caller explicitly requests the
        templates (`force`). Otherwise all fidelity checks are skipped.
        """
        self.issues = []

        if not self._should_enforce_fidelity():
            return self.issues

        # Determine template and rules files
        template_map = {
            "ARCHITECTURE.md": ("architecture.md", "architecture.md"),
            "CODE_OF_CONDUCT.md": ("code-of-conduct.md", "code-of-conduct.md"),
            "CONTRIBUTING.md": ("contributing.md", "contributing.md"),
            "PRIVACY.md": ("privacy.md", "privacy.md"),
            "README.md": ("readme.md", "readme.md"),
            "ROADMAP.md": ("roadmap.md", "roadmap.md"),
            "SECURITY.md": ("security.md", "security.md"),
        }

        if target_file not in template_map:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Unknown target file: {target_file}"
            ))
            return self.issues

        template_file, rules_file = template_map[target_file]
        template_path = self.templates_dir / template_file
        rules_path = self.rules_dir / rules_file

        if not template_path.exists():
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Template not found: {template_path}"
            ))
            return self.issues

        if not rules_path.exists():
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Rules not found: {rules_path}"
            ))
            return self.issues

        # Read the template that the document must follow
        template_content = template_path.read_text(encoding='utf-8')

        # Run validation checks
        self._check_placeholders_removed(generated_content)
        self._check_template_comments_removed(generated_content)
        self._check_toc_entries(generated_content)
        self._check_mandatory_headings(generated_content, template_content)
        self._check_empty_sections(generated_content)
        self._check_fixed_prose_integrity(generated_content, template_content)

        return self.issues

    def _should_enforce_fidelity(self) -> bool:
        """Return True when the document must follow the templates verbatim.

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

        owner = GitHubMDValidator._extract_owner(remote)
        self._resolved_owner = owner

        return owner

    def _get_current_git_user(self) -> Optional[str]:
        """Return the current git/GitHub user login, or None if unknown.

        Resolution order prefers authenticated identity, then explicit Git
        configuration, then the GitHub login embedded in a `users.noreply`
        commit e-mail. Display names are never used because they are not
        account logins.
        """
        if self._resolved_git_user is not None:
            return self._resolved_git_user

        login = self._run_read_only_query(["gh", "api", "user", "--jq", ".login"])

        if not login:
            login = self._run_read_only_query(["git", "config", "--get", "github.user"])

        if not login:
            email = self._run_read_only_query(["git", "config", "--get", "user.email"])
            login = GitHubMDValidator._extract_noreply_login(email or "")

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

        # Prefer the GitHub API (authenticated or unauthenticated) so the
        # result reflects the real owner type rather than URL heuristics.
        # Query the owner account endpoint: users/{owner} returns "type" of
        # "User" or "Organization" (and 404s for unknown owners).
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

        # SSH form: git@github.com:owner/repo.git
        ssh_match = re.match(r"git@[^:]+:([^/]+)/", remote_url)
        if ssh_match:
            return ssh_match.group(1)

        # HTTPS form: https://github.com/owner/repo.git
        https_match = re.match(r"https?://[^/]+/([^/]+)/", remote_url)
        if https_match:
            return https_match.group(1)

        return None

    def _check_placeholders_removed(self, content: str):
        """Check that no [[PLACEHOLDER]] or [[[PLACEHOLDER]]] remain."""
        # Double bracket placeholders
        double_brackets = re.findall(r'\[\[([A-Z_]+)\]\]', content)
        for ph in double_brackets:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Unresolved placeholder: [[{ph}]]",
                context=f"Found unresolved scalar placeholder"
            ))

        # Triple bracket placeholders
        triple_brackets = re.findall(r'\[\[\[([^\]]+)\]\]\]', content)
        for ph in triple_brackets:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Unresolved block placeholder: [[[{ph}]]]",
                context=f"Found unresolved block placeholder"
            ))

    def _check_template_comments_removed(self, content: str):
        """Check that no template comments remain."""
        template_comments = re.findall(r'<!--\s*(Only if|Always include|Generate one entry|Repeat for each|Add, combine, or remove|Include when|Use this subsection|Add additional rows).*?-->', content, re.DOTALL)
        for comment in template_comments:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Template comment not removed: {comment[:100]}...",
                context="Template directive comment found in output"
            ))

    def _check_toc_entries(self, content: str):
        """Check the Table of Contents for emojis, coverage, and order."""
        toc_match = re.search(r'(?:^|\n)#{1,6}\s*\S*\s*Table of Contents\s*\n(.*?)(?=\n#{1,6}\s|\Z)', content, re.DOTALL)

        if not toc_match:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Table of Contents section missing",
                context="Required ToC section not found"
            ))
            return

        toc_entries = [
            (label, anchor)
            for label, anchor in re.findall(r'^\s*-\s*\[([^\]]+)\]\(#([^\)]*)\)\s*$', toc_match.group(1), re.MULTILINE)
        ]

        for label, _ in toc_entries:
            if self._strip_heading_markers(label).lower() == 'table of contents':
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    "Table of Contents lists itself as an entry",
                    context="Do not include the Table of Contents heading in its own list"
                ))

            if re.search(r'[\U0001F300-\U0001FAFF\u2190-\u2BFF\uFE0F]', label):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Emoji found in ToC entry: {label}",
                    context="Table of Contents must not contain emojis in entry text"
                ))

        entries_without_self = [
            (self._strip_heading_markers(label), anchor)
            for label, anchor in toc_entries
            if self._strip_heading_markers(label).lower() != 'table of contents'
        ]

        expected_anchors = []
        body_headings = []
        in_code_block = False

        for line in content.splitlines():
            stripped = line.strip()

            if stripped.startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block or not re.match(r'^#{2,4}\s', stripped):
                continue

            heading = self._strip_heading_markers(stripped)

            if heading.lower() == 'table of contents':
                continue

            body_headings.append(heading)
            expected_anchors.append(self._slugify(heading))

        labels = [label for label, _ in entries_without_self]
        anchors = [anchor for _, anchor in entries_without_self]

        for heading, anchor in zip(body_headings, expected_anchors):
            if anchor not in anchors:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Heading missing from Table of Contents: {heading}",
                    context="Every ##, ###, and #### heading must appear in the ToC"
                ))

            elif heading not in labels:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"ToC entry text does not match its heading: {heading}",
                    context="ToC labels must reproduce the heading text without emojis"
                ))

        observed = [anchor for anchor in anchors if anchor in expected_anchors]

        if observed != expected_anchors:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Table of Contents entries are missing or out of document order",
                context=f"Expected order: {expected_anchors}"
            ))

    @staticmethod
    def _strip_heading_markers(text: str) -> str:
        """Return heading or label text with leading Markdown markers removed."""
        without_emojis = re.sub(r'[\U0001F300-\U0001FAFF\u2190-\u2BFF\uFE0F]', '', text)
        without_hashes = re.sub(r'^#+\s*', '', without_emojis.strip())

        return re.sub(r'\s+', ' ', without_hashes).strip()

    @staticmethod
    def _slugify(heading: str) -> str:
        """Return the GitHub-style anchor slug for a heading's plain text.

        Emoji and punctuation are removed, spaces become hyphens, and repeated
        or leading hyphens are collapsed so that both the ``#-heading`` and
        ``#heading`` conventions compare equal.
        """
        lowered = heading.lower()
        without_punctuation = re.sub(r'[^\w\s-]', '', lowered)
        hyphenated = re.sub(r'\s+', '-', without_punctuation.strip())

        return re.sub(r'-{2,}', '-', hyphenated).strip('-')

    def _check_mandatory_headings(self, content: str, template_content: str):
        """Check that every non-conditional template heading survives verbatim."""
        template_lines = self._strip_front_matter(template_content).splitlines()
        gated_indices = self._get_conditional_indices(template_lines)
        document_headings = {
            self._normalise_prose(line)
            for line in content.splitlines()
            if HEADING_PATTERN.match(line.strip())
        }
        in_code_block = False

        for index, template_line in enumerate(template_lines):
            stripped = template_line.strip()

            if stripped.startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block or index in gated_indices:
                continue

            heading = self._normalise_prose(template_line)

            if not HEADING_PATTERN.match(heading) or heading in document_headings:
                continue

            # Headings that embed placeholders are rendered, not copied verbatim.
            if PLACEHOLDER_PATTERN.search(template_line):
                continue

            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Mandatory heading missing or changed: {heading}",
                line_number=index + 1,
                context="Non-conditional template headings must appear verbatim"
            ))

    def _check_empty_sections(self, content: str):
        """Check for empty headings, tables, and code blocks."""
        lines = content.split('\n')
        in_code_block = False
        code_block_start = -1

        for i, line in enumerate(lines):
            stripped = line.strip()

            if stripped.startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_start = i
                else:
                    in_code_block = False

                    if i == code_block_start + 1:
                        self.issues.append(ValidationIssue(
                            ValidationSeverity.ERROR,
                            f"Empty code block at line {i+1}",
                            context="Code blocks must have content"
                        ))

                continue

            if in_code_block:
                continue

            # A heading is empty only when no content and no subsection follow it.
            heading_match = re.match(r'^(#{1,6})\s+.+', stripped)

            if heading_match:
                heading_level = len(heading_match.group(1))
                has_content = False

                for subsequent in lines[i + 1:]:
                    subsequent_stripped = subsequent.strip()

                    if not subsequent_stripped:
                        continue

                    nested_match = re.match(r'^(#{1,6})\s+', subsequent_stripped)

                    if nested_match and len(nested_match.group(1)) > heading_level:
                        has_content = True
                        break

                    if nested_match:
                        break

                    has_content = True
                    break

                if not has_content:
                    self.issues.append(ValidationIssue(
                        ValidationSeverity.WARNING,
                        f"Empty section at line {i+1}: {stripped}",
                        context="Section has no content and no subsections"
                    ))

        # A table is empty only when it has a header, a separator, and no data row.
        for index, line in enumerate(lines):
            if not self._is_table_row(line):
                continue

            if index > 0 and self._is_table_row(lines[index - 1]):
                continue

            if index + 1 >= len(lines) or not self._is_table_separator(lines[index + 1]):
                continue

            if index + 2 < len(lines) and self._is_table_row(lines[index + 2]):
                continue

            self.issues.append(ValidationIssue(
                ValidationSeverity.WARNING,
                f"Empty table at line {index + 1}",
                context="Table has a header and separator but no data rows"
            ))

    @staticmethod
    def _is_table_row(line: str) -> bool:
        """Report whether a line is a Markdown table row."""
        return line.strip().startswith('|')

    @staticmethod
    def _is_table_separator(line: str) -> bool:
        """Report whether a line is a Markdown table separator row."""
        stripped = line.strip()

        if not stripped.startswith('|'):
            return False

        cells = [cell.strip() for cell in stripped.strip('|').split('|')]

        return bool(cells) and all(re.fullmatch(r':?-{3,}:?', cell) for cell in cells)

    def _check_fixed_prose_integrity(self, content: str, template_content: str):
        """Check that fixed template prose survives into the generated document.

        Conditional blocks may legitimately be omitted. A block is treated as
        included when its heading, or its first placeholder-free prose line,
        appears in the generated document. Lines carrying placeholders or inline
        conditional directives are not fixed prose and are skipped.
        """
        template_lines = self._strip_front_matter(template_content).splitlines()
        blocks = self._get_conditional_blocks(template_lines)
        document_prose = self._normalise_prose(content)
        unique_blocks = sorted(set(blocks.values()))
        heading_counts = collections.Counter()
        block_headings = {}

        for start, end in unique_blocks:
            heading_match = HEADING_PATTERN.match(template_lines[start].strip())

            if heading_match is not None:
                heading_text = self._normalise_prose(template_lines[start])
                heading_counts[heading_text] += 1
                block_headings[(start, end)] = heading_text

        skipped = set()

        for start, end in unique_blocks:
            heading_text = block_headings.get((start, end))
            shares_heading = heading_text is not None and heading_counts[heading_text] > 1

            if not self._is_block_included(template_lines, start, end, document_prose, shares_heading):
                skipped.update(range(start, end))

        body_start = self._get_body_start_index(template_lines)
        in_code_block = False

        for index in range(body_start, len(template_lines)):
            template_line = template_lines[index]
            stripped = template_line.strip()

            if stripped.startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block or index in skipped:
                continue

            prose = self._normalise_prose(template_line)

            if not self._is_fixed_prose(template_line, prose):
                continue

            skeleton, fixed_words = self._prose_skeleton(prose)

            if fixed_words < 4:
                continue

            if re.search(skeleton, document_prose) is None:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Fixed template prose changed or missing: {prose}",
                    line_number=index + 1,
                    context="Only placeholders and HTML comments may be changed"
                ))

    @staticmethod
    def _prose_skeleton(prose: str) -> tuple:
        """Build a regular expression from prose, treating placeholders as wildcards.

        Returns the expression together with the number of fixed (non-placeholder)
        words that must survive into the generated document.
        """
        parts = []
        fixed_words = 0
        position = 0

        for match in PLACEHOLDER_PATTERN.finditer(prose):
            literal = prose[position:match.start()]
            parts.append(re.escape(literal))
            fixed_words += len(literal.split())
            parts.append('.{0,400}?')
            position = match.end()

        tail = prose[position:]
        parts.append(re.escape(tail))
        fixed_words += len(tail.split())

        return ''.join(parts), fixed_words

    @classmethod
    def _is_block_included(
        cls,
        template_lines: List[str],
        start: int,
        end: int,
        document_prose: str,
        require_distinguishing_line: bool = False,
    ) -> bool:
        """Report whether a conditional block is present in the document.

        A block without a distinguishing body sentence counts as included when
        its heading appears in the generated document. When the block owns at
        least one placeholder-free body sentence, that sentence decides
        inclusion in place of the heading, which keeps mutually exclusive
        variants that share a heading distinguishable.
        """
        heading_present = False
        body_sentences = []

        for offset in range(start, end):
            template_line = template_lines[offset]
            candidate = template_line.strip()

            if not candidate:
                continue

            prose = cls._normalise_prose(template_line)

            if not prose:
                continue

            if HEADING_PATTERN.match(prose):
                if prose in document_prose:
                    heading_present = True

                continue

            if candidate.startswith('|') or PLACEHOLDER_PATTERN.search(template_line):
                continue

            if len(prose.split()) < 4:
                continue

            body_sentences.append(prose)

        if body_sentences and (require_distinguishing_line or not heading_present):
            return any(sentence in document_prose for sentence in body_sentences)

        return heading_present

    @staticmethod
    def _get_body_start_index(template_lines: List[str]) -> int:
        """Return the index of the first document heading, skipping template prose."""
        for index, template_line in enumerate(template_lines):
            if HEADING_PATTERN.match(template_line.strip()):
                return index

        return 0

    @staticmethod
    def _is_fixed_prose(template_line: str, prose: str) -> bool:
        """Report whether a template line is comparable fixed prose.

        Lines carrying a conditional directive anywhere, including inline
        directives attached to a bullet or sentence, are excluded because the
        directive governs whether the text is emitted at all. Table rows are
        excluded because their cells are data rather than fixed prose.
        """
        if not prose:
            return False

        if INLINE_CONDITIONAL_PATTERN.search(template_line):
            return False

        if HEADING_PATTERN.match(prose):
            return True

        if prose.startswith('|'):
            return False

        if PLACEHOLDER_PATTERN.search(prose):
            skeleton, fixed_words = GitHubMDValidator._prose_skeleton(prose)

            return fixed_words >= 4 and bool(skeleton)

        return len(prose.split()) >= 4

    @staticmethod
    def _normalise_prose(text: str) -> str:
        """Collapse prose to a single comparable form."""
        without_comments = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
        collapsed = re.sub(r'\s+', ' ', without_comments).strip()

        return LIST_MARKER_PATTERN.sub('', collapsed).strip()

    @staticmethod
    def _strip_front_matter(content: str) -> str:
        """Return content without its leading YAML front matter."""
        lines = content.splitlines()

        if lines and lines[0].strip() == '---':
            for index in range(1, len(lines)):
                if lines[index].strip() == '---':
                    return '\n'.join(lines[index + 1:])

        return content

    @staticmethod
    def _get_conditional_blocks(template_lines: List[str]) -> dict:
        """Return conditional blocks as ``{gated index: (start, end)}`` pairs.

        A block starts at the first non-blank line after a directive-only
        comment and ends before the next directive or the next heading at the
        same or a shallower level. Standalone headings that are immediately
        followed by a directive are themselves gated.
        """
        blocks = {}

        for index, template_line in enumerate(template_lines):
            if not CONDITIONAL_DIRECTIVE_PATTERN.search(template_line):
                continue

            if re.sub(r'<!--.*?-->', '', template_line, flags=re.DOTALL).strip():
                continue

            start = None

            for offset in range(index + 1, len(template_lines)):
                if template_lines[offset].strip():
                    start = offset
                    break

            if start is None:
                continue

            heading_match = HEADING_PATTERN.match(template_lines[start].strip())
            end = len(template_lines)

            if heading_match is not None:
                heading_level = len(heading_match.group(1))

                for offset in range(start + 1, len(template_lines)):
                    nested_match = HEADING_PATTERN.match(template_lines[offset].strip())

                    if nested_match and len(nested_match.group(1)) <= heading_level:
                        end = offset
                        break
            else:
                for offset in range(start + 1, len(template_lines)):
                    if CONDITIONAL_DIRECTIVE_PATTERN.search(template_lines[offset]):
                        end = offset
                        break

                    if HEADING_PATTERN.match(template_lines[offset].strip()):
                        end = offset
                        break

            for offset in range(start, end):
                blocks[offset] = (start, end)

        for index, template_line in enumerate(template_lines):
            if not HEADING_PATTERN.match(template_line.strip()):
                continue

            for offset in range(index + 1, len(template_lines)):
                if not template_lines[offset].strip():
                    continue

                if CONDITIONAL_DIRECTIVE_PATTERN.search(template_lines[offset]):
                    blocks.setdefault(index, (index, index + 1))

                break

        return blocks

    @staticmethod
    def _get_conditional_indices(template_lines: List[str]) -> Set[int]:
        """Return template line indices governed by a conditional directive."""
        return set(GitHubMDValidator._get_conditional_blocks(template_lines).keys())

    @staticmethod
    def _remove_html_comments(content: str) -> str:
        """Remove template comments before comparing generated prose."""
        return re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)


def main():
    args = sys.argv[1:]
    force = os.environ.get("GITHUB_MD_FORCE_FIDELITY", "").strip().lower() in {"1", "true", "yes"}

    if args and args[0] in ("--force", "--use-templates"):
        force = True
        args = args[1:]

    if len(args) < 2:
        print("Usage: validate_github_md.py [--force] <repo_root> <target_file> [generated_file]")
        print("  If generated_file not provided, reads from stdin")
        print("  --force: enforce template fidelity regardless of repository ownership")
        sys.exit(2)

    repo_root = Path(args[0])
    target_file = args[1]

    if len(args) > 2:
        generated_content = Path(args[2]).read_text(encoding='utf-8')
    else:
        generated_content = sys.stdin.read()

    validator = GitHubMDValidator(repo_root, force=force)
    issues = validator.validate(target_file, generated_content)

    # Template fidelity is enforced only for personal repositories owned by the
    # current git user, unless the templates were explicitly requested.
    if not validator._should_enforce_fidelity():
        print("ℹ️  Template fidelity enforcement skipped: repository is not a personal "
              "repository owned by the current git user. Pass --force (or set "
              "GITHUB_MD_FORCE_FIDELITY=1) when the templates are explicitly requested.")
        sys.exit(3)

    # Output results
    errors = [i for i in issues if i.severity == ValidationSeverity.ERROR]
    warnings = [i for i in issues if i.severity == ValidationSeverity.WARNING]

    if errors:
        print(f"❌ VALIDATION FAILED: {len(errors)} errors, {len(warnings)} warnings")
        for issue in errors:
            print(f"  ERROR: {issue.message}")
            if issue.context:
                print(f"    Context: {issue.context}")
        sys.exit(1)
    elif warnings:
        print(f"⚠️  VALIDATION PASSED WITH WARNINGS: {len(warnings)} warnings")
        for issue in warnings:
            print(f"  WARNING: {issue.message}")
            if issue.context:
                print(f"    Context: {issue.context}")
        sys.exit(0)
    else:
        print("✅ VALIDATION PASSED: 100% template fidelity confirmed")
        sys.exit(0)


if __name__ == "__main__":
    main()