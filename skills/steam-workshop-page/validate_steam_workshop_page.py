#!/usr/bin/env python3
"""
Steam Workshop Page Description Template Fidelity Validator
Validates generated Steam Workshop BBCode descriptions against the canonical
template for 100% fidelity.
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Set
from dataclasses import dataclass
from enum import Enum

TEMPLATE_FILE = "workshop-description.bbcode"
RULES_FILE = "workshop-description.md"

PLACEHOLDER_PATTERN = re.compile(r'\[\[[A-Z0-9_]+\]\]')
LINK_FILTER_PREFIX = "https://steamcommunity.com:/linkfilter/?url="
# Matches a link-filtered URL target, tolerating a `[[PLACEHOLDER]]` value.
LINK_FILTER_TARGET = r'(?:\[\[[A-Z0-9_]+\]\]|[^\]\n])+'
MARKDOWN_PATTERN = re.compile(
    r'(?:^|\s)(?:#{1,6}\s|[-*+]\s+\S|\*\*[^*]+\*\*|`[^`]+`|\[[^\]\n]+\]\([^)\n]+\))'
)
RAW_HTML_PATTERN = re.compile(r'<\s*(?:a|p|div|span|b|i|u|img|br|h[1-6]|script)\b', re.IGNORECASE)
HIDDEN_TEXT_PATTERN = re.compile(
    r'\[color=transparent\]|\[color=#?000000\]|\[size=1px\]|display\s*:\s*none',
    re.IGNORECASE,
)

# Fixed template fragments that must survive generation byte-for-byte.
FIXED_FRAGMENTS = (
    "[img]https://i.imgur.com/8I8Im27.gif[/img]",
    "[img]https://i.imgur.com/ZW5bp28.png[/img] [/url]",
    "[img]https://i.imgur.com/UPNlpGj.png[/img][/url]",
    "/announcement_donation.png[/img][/url]",
    "/banner_donate.png[/img][/url]",
)

# Mandatory sections, in the required order.
MANDATORY_SECTIONS = (
    "About",
    "Capabilities",
    "Installation",
    "Support",
    "Project Engagement",
    "License",
)
H1_PATTERN = re.compile(r'\[h1\](.*?)\[/h1\]', re.IGNORECASE)
H2_PATTERN = re.compile(r'\[h2\](.*?)\[/h2\]', re.IGNORECASE)

# Canonical output path, relative to the repository root.
OUTPUT_DIRECTORY = "description"
OUTPUT_FILE_NAME = "steam-workshop.bbcode"
OUTPUT_RELATIVE_PATH = f"{OUTPUT_DIRECTORY}/{OUTPUT_FILE_NAME}"

# Section headings permitted between the mandatory sections.
KNOWN_OPTIONAL_SECTIONS = {
    "Capabilities",
    "Installation",
    "Upgrading",
    "Requirements",
    "Compatibility",
    "Related Mods",
    "Contributing",
}

MAX_CAPABILITY_ITEMS = 12
RELATED_MODS_HEADING = "Related Mods"
MANUAL_INSTALLATION_HEADING = "Manual Installation"
# Sections that must never appear standalone; their content lives elsewhere.
MERGED_SECTION_HEADINGS = {
    "Troubleshooting": "Support",
    "FAQ": "Support",
    "Changelog": None,
    "Localisation": "Compatibility",
}
DISALLOWED_SUBHEADINGS = {
    "Manual Installation": None,
    "Uninstallation": None,
}

# Template comment shapes: `<!-- Only if ... -->`, `<!-- Repeat ... -->`.
TEMPLATE_COMMENT_PATTERN = re.compile(r'<!--.*?-->', re.DOTALL)

BADGE_STORE_PREFIX = (
    "https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/"
)
BADGE_PATTERN = re.compile(
    r'\[url=([^\]]+)\]\[img\]https://raw\.githubusercontent\.com/'
    r'hmlendea/readme-assets/master/badges/stores/([a-z0-9\-]+)\.png\[/img\]\[/url\]'
)
MAX_BADGES_PER_LINE = 3
BADGE_LINE_PREFIX = "    "
STEAM_URL_PREFIX = "https://steamcommunity.com/"
# Placeholder-free store badge shape, used to detect misplaced badge paths.
BADGE_PATH_PATTERN = re.compile(
    r'raw\.githubusercontent\.com/hmlendea/readme-assets/master/(?!badges/stores/)[^\s\[]*badge[^\s\[]*',
    re.IGNORECASE,
)
SUPPORT_FIXED_SENTENCE = (
    "]GitHub[/url]. None of the other channels are actively monitored, "
    "which may result in delayed responses."
)
SUPERSEDED_SUPPORT_SENTENCE = "GitHub is the primary location for obtaining support"
CONTRIBUTING_FIXED_SENTENCE = (
    "See the [url=<CONTRIBUTING_URL>]Contributing Guidelines[/url] for details on how "
    "to report issues, suggest enhancements, and submit changes."
)
TROUBLESHOOTING_FIXED_SENTENCE = (
    "]Troubleshooting Guide[/url] for diagnostic procedures and resolutions to "
    "recurring problems."
)
SUPERSEDED_CONTRIBUTING_SENTENCE = "Contributions are managed on the"
SUPERSEDED_CONTRIBUTING_ISSUE_SENTENCE = (
    "To report a problem or suggest an enhancement, submit an"
)


def _balanced_badge_layout(total: int) -> list:
    """Distribute badges across the fewest lines, as evenly as possible.

    Three badges fill one line and four badges are laid out two per line. In
    general the badges occupy ``ceil(total / 3)`` lines, spread as evenly as
    possible with any remainder on the earlier lines.
    """
    if total <= 0:
        return []

    lines = -(-total // MAX_BADGES_PER_LINE)
    base, extra = divmod(total, lines)

    return [base + 1 if index < extra else base for index in range(lines)]


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


class SteamWorkshopPageValidator:
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

    def validate(self, generated_content: str) -> List[ValidationIssue]:
        """Validate a generated Workshop description against the template.

        Template fidelity is enforced only for personal repositories owned by
        the current git user, or whenever the caller explicitly requests the
        template (`force`). Otherwise all fidelity checks are skipped.
        """
        self.issues = []

        if not self._should_enforce_fidelity():
            return self.issues

        template_path = self.templates_dir / TEMPLATE_FILE
        rules_path = self.rules_dir / RULES_FILE

        if not template_path.exists():
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Template not found: {template_path}",
            ))
            return self.issues

        if not rules_path.exists():
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Rules not found: {rules_path}",
            ))
            return self.issues

        template_content = template_path.read_text(encoding='utf-8')

        self._check_placeholders_removed(generated_content)
        self._check_template_comments_removed(generated_content)
        self._check_header_and_footer(generated_content)
        self._check_fixed_fragments(generated_content)
        self._check_template_fixed_lines(generated_content, template_content)
        self._check_mandatory_sections(generated_content)
        self._check_installation_badges(generated_content)
        self._check_link_filtering(generated_content)
        self._check_bbcode_only(generated_content)
        self._check_hidden_text(generated_content)
        self._check_bracket_balance(generated_content)

        return self.issues

    def _check_template_comments_removed(self, content: str):
        """Check that no template directive comment survives in the output."""
        for match in TEMPLATE_COMMENT_PATTERN.finditer(content):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Template comment not removed: {match.group(0)[:80]}",
                context="Strip every template directive comment from the delivered description",
            ))

    def _check_template_fixed_lines(self, content: str, template_content: str):
        """Check that fixed template lines survive into the description.

        Lines carrying placeholders and every line gated by a template directive
        comment may legitimately change or be removed, so they are excluded from
        comparison. Everything else is fixed prose that must appear verbatim.
        """
        template_lines = template_content.splitlines()
        gated = self._get_gated_indices(template_lines)

        for index, template_line in enumerate(template_lines):
            if index in gated:
                continue

            stripped = template_line.strip()

            if not stripped:
                continue

            if PLACEHOLDER_PATTERN.search(stripped):
                continue

            if stripped not in content:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Fixed template line changed or missing: {stripped}",
                    line_number=index + 1,
                    context="Only placeholders, Repeat examples, and conditional blocks may change",
                ))

    @staticmethod
    def _get_gated_indices(template_lines: List[str]) -> Set[int]:
        """Return template line indices governed by a directive comment.

        A directive comment gates itself and the contiguous block that follows it
        up to the next blank line, the next directive comment, or the next heading
        that the comment does not introduce.
        """
        gated = set()

        for index, line in enumerate(template_lines):
            if not TEMPLATE_COMMENT_PATTERN.search(line):
                continue

            gated.add(index)
            cursor = index + 1

            while cursor < len(template_lines):
                current = template_lines[cursor]

                if not current.strip():
                    gated.add(cursor)
                    break

                if TEMPLATE_COMMENT_PATTERN.search(current):
                    break

                gated.add(cursor)
                cursor += 1

                # A heading introduced by the comment closes the gated block once
                # its own single body line has been consumed.
                if H1_PATTERN.search(current) or H2_PATTERN.search(current):
                    break

        return gated

    def _should_enforce_fidelity(self) -> bool:
        """Return True when the description must follow the template verbatim.

        Enforcement applies when the caller explicitly requests the template
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

        remote = self._get_origin_remote()

        if not remote:
            return None

        self._resolved_owner = SteamWorkshopPageValidator._extract_owner(remote)

        return self._resolved_owner

    def _get_origin_remote(self) -> Optional[str]:
        """Return the raw `origin` remote URL, or None."""
        try:
            result = subprocess.run(
                ["git", "-C", str(self.repo_root), "remote", "get-url", "origin"],
                capture_output=True, text=True, timeout=10,
            )
        except (OSError, subprocess.SubprocessError):
            return None

        return result.stdout.strip() or None

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
            login = SteamWorkshopPageValidator._extract_noreply_login(email or "")

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
            self._resolved_owner_type = api_result.stdout.strip()
            return self._resolved_owner_type

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
        """Check that no [[PLACEHOLDER]] tokens remain."""
        for placeholder in PLACEHOLDER_PATTERN.findall(content):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Unresolved placeholder: {placeholder}",
                context="Found unresolved placeholder in Workshop description",
            ))

    def _check_header_and_footer(self, content: str):
        """Check that the description opens and closes with the fixed blocks."""
        stripped = content.strip()

        first_line = stripped.splitlines()[0] if stripped else ""

        if not first_line.startswith("[img]https://i.imgur.com/8I8Im27.gif[/img]"):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Description does not open with the header banner block",
                line_number=1,
                context="The first line must start with the fixed header animation image",
            ))

        if not re.search(r'\[url=https://steamcommunity\.com:/linkfilter/\?url=' + LINK_FILTER_TARGET + r'\]\[img\]https://i\.imgur\.com/ZW5bp28\.png\[/img\]\s*\[/url\]', first_line):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Header funding button missing or altered",
                line_number=1,
                context="The fixed funding button image and link-filtered URL must be preserved",
            ))

        if not re.search(r'\[url=https://steamcommunity\.com:/linkfilter/\?url=' + LINK_FILTER_TARGET + r'\]\[img\]https://i\.imgur\.com/UPNlpGj\.png\[/img\]\[/url\]', first_line):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Header repository button missing or altered",
                line_number=1,
                context="The fixed repository button image and link-filtered URL must be preserved",
            ))

        lines = stripped.splitlines() if stripped else []
        last_line = lines[-1] if lines else ""

        if not re.search(r'^\[url=https://steamcommunity\.com:/linkfilter/\?url=' + LINK_FILTER_TARGET + r'\]\[img\]' + LINK_FILTER_TARGET + r'/banner_donate\.png\[/img\]\[/url\]$', last_line):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Description does not end with the closing donate banner",
                line_number=len(lines) or None,
                context="The final content line must be the fixed link-filtered donate banner",
            ))

        if not re.search(r'\[url=https://steamcommunity\.com:/linkfilter/\?url=' + LINK_FILTER_TARGET + r'\]\[img\]' + LINK_FILTER_TARGET + r'/announcement_donation\.png\[/img\]\[/url\]', stripped):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Announcement donation banner missing or altered",
                context="The fixed link-filtered announcement banner must follow the header block",
            ))

    def _check_fixed_fragments(self, content: str):
        """Check that every fixed template fragment is present verbatim."""
        for fragment in FIXED_FRAGMENTS:
            if fragment not in content:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Fixed template fragment missing or altered: {fragment}",
                    context="Fixed template content must be copied byte-for-byte",
                ))

    def _check_mandatory_sections(self, content: str):
        """Check the mandatory sections, their order, and their fixed prose."""
        headings = [match.strip() for match in H1_PATTERN.findall(content)]
        positions = []

        for section in MANDATORY_SECTIONS:
            matches = [index for index, heading in enumerate(headings) if heading == section]

            if not matches:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Mandatory section missing: [{section}]",
                    context="About, Capabilities, Installation, Contributing, Support, "
                            "Project Engagement, and License are mandatory and must use a "
                            "fixed [h1] heading",
                ))
                positions.append(-1)
                continue

            if len(matches) > 1:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Mandatory section duplicated: [{section}]",
                    context="Each mandatory section may appear exactly once",
                ))

            positions.append(matches[0])

        present = [position for position in positions if position >= 0]

        if present and present != sorted(present):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Mandatory sections are out of order",
                context="Required order: About, Capabilities, Installation, Contributing, "
                        "Support, Project Engagement, License",
            ))

        for heading in headings:
            if heading not in MANDATORY_SECTIONS and heading not in KNOWN_OPTIONAL_SECTIONS:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.WARNING,
                    f"Section heading is not in the section contract: [{heading}]",
                    context="Sections must come from the documented mandatory or optional list",
                ))

        contributing_index = headings.index("Contributing") if "Contributing" in headings else -1
        support_index = headings.index("Support") if "Support" in headings else -1

        if contributing_index >= 0 and support_index > contributing_index:
            between = headings[contributing_index + 1:support_index]

            for heading in between:
                if heading != RELATED_MODS_HEADING:
                    self.issues.append(ValidationIssue(
                        ValidationSeverity.ERROR,
                        f"Section placed between Contributing and Support is not permitted "
                        f"there: [{heading}]",
                        context="Only the conditional Related Mods section may precede Support",
                    ))

        self._check_capabilities_section(content)
        self._check_installation_subheadings(content)
        self._check_compatibility(content)
        self._check_merged_sections(content)
        self._check_contributing_section(content)
        self._check_troubleshooting_sentence(content)
        self._check_project_engagement(content)
        self._check_license_section(content)
        self._check_related_mods(content)

    def _check_capabilities_section(self, content: str):
        """Check that the Capabilities section carries a bounded, non-vacant list."""
        body = self._extract_section_body(content, "Capabilities")

        if body is None:
            return

        if not re.search(r'\[list\]', body, re.IGNORECASE):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Capabilities section has no BBCode list",
                context="Capabilities is a heading followed by a single [list] of [*] items",
            ))
            return

        items = [
            item.strip()
            for item in re.findall(r'\[\*\](.*?)(?=\[\*\]|\[/list\]|\Z)', body, re.DOTALL)
        ]
        items = [item for item in items if item]

        if not items:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Capabilities section has a vacant list",
                context="Emit one [*] item per evidenced capability",
            ))
            return

        if len(items) > MAX_CAPABILITY_ITEMS:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Capabilities section carries {len(items)} items; the maximum is "
                f"{MAX_CAPABILITY_ITEMS}",
                context="Keep only the principal, evidenced capabilities",
            ))

    def _check_installation_subheadings(self, content: str):
        """Check that Installation carries no Manual Installation or Uninstallation."""
        body = self._extract_section_body(content, "Installation")

        if body is None:
            return

        for heading in DISALLOWED_SUBHEADINGS:
            if re.search(rf'\[h2\]\s*{re.escape(heading)}\s*\[/h2\]', body, re.IGNORECASE):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Disallowed Installation sub-section: [h2]{heading}[/h2]",
                    context="Installation carries only the badges and the conditional Upgrading "
                            "sub-section",
                ))

        upgrade = re.search(r'\[h2\]\s*Upgrading\s*\[/h2\](.*?)(?=\[h2\]|\[h1\]|\Z)',
                            body, re.IGNORECASE | re.DOTALL)

        if upgrade and not upgrade.group(1).strip():
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Upgrading sub-section has no content",
                context="Never emit a vacant Upgrading heading",
            ))

    def _check_merged_sections(self, content: str):
        """Check that merged sections do not appear standalone.

        Troubleshooting, FAQ, Changelog, and Localisation must never be standalone
        headings; their content lives inside Support or Compatibility.
        """
        headings = [match.strip() for match in H1_PATTERN.findall(content)]

        for heading in headings:
            if heading in MERGED_SECTION_HEADINGS:
                destination = MERGED_SECTION_HEADINGS[heading]

                if destination is None:
                    self.issues.append(ValidationIssue(
                        ValidationSeverity.ERROR,
                        f"Section must not exist: [{heading}]",
                        context="This section was removed from the template contract",
                    ))
                    continue

                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Section must not be standalone: [{heading}]",
                    context=f"Its content belongs inside {destination}",
                ))

        support = self._extract_section_body(content, "Support")

        if support is not None:
            if not re.search(re.escape(SUPPORT_FIXED_SENTENCE), support):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    "Support section is missing the fixed issue-tracker sentence",
                    context="The sentence must end: [url=<REPO>]GitHub[/url] on GitHub. "
                            "None of the other channels are actively monitored, which "
                            "may result in delayed responses.",
                ))

            if re.search(re.escape(SUPERSEDED_SUPPORT_SENTENCE), support):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    "Support section carries the superseded GitHub-primary sentence",
                    context="It is merged into the preceding sentence as "
                            "`on GitHub. None of the other channels are actively "
                            "monitored, which may result in delayed responses.`",
                ))

            faq = re.search(r'See the \[url=[^\]]+\]FAQ\[/url\] for responses to frequent inquiries\.', support)

            if faq is None and re.search(r'\[url=[^\]]+\]FAQ\[/url\]', support):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    "Support FAQ sentence does not match the fixed wording",
                    context="Expected: See the [url=<FAQ_URL>]FAQ[/url] for responses to "
                            "frequent inquiries.",
                ))

    def _check_compatibility(self, content: str):
        """Check the fixed Compatibility prose when the section is included."""
        body = self._extract_section_body(content, "Compatibility")

        if body is None:
            return

        if not body.strip():
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Compatibility section has no content",
                context="Never emit a vacant Compatibility heading",
            ))
            return

        sentence = re.search(
            r'This mod is compatible with ([^\n.\[]+?) '
            r'([^\s.\[]*[0-9][^\s.\[]*)[^\n]*? on all operating systems\.',
            body,
            re.IGNORECASE,
        )

        if sentence is None:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Compatibility section is missing the unified compatibility sentence",
                context="Use: This mod is compatible with <GAME_NAME> "
                        "<SUPPORTED_GAME_VERSION> on all operating systems.",
            ))
        elif not sentence.group(1).strip():
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Unified compatibility sentence has no game name",
                context="Name the game the mod targets, for example Stellaris",
            ))

        if re.search(r'\[b\]OS-agnostic\[/b\]|\bworks on any operating system\b',
                     body, re.IGNORECASE):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Compatibility section carries the superseded OS-agnostic paragraph",
                context="It was replaced by the unified compatibility sentence",
            ))

        if re.search(r'\bgame version\s*:|\bTarget game version\b', body, re.IGNORECASE):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Compatibility section carries the superseded game-version block",
                context="The version is embedded in the unified compatibility sentence",
            ))

        if re.search(r'\[code\][^\[]*\d[^\[]*\[/code\]', body, re.IGNORECASE):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Version is enclosed in [code][/code]",
                context="Enclose versions in [b][/b] instead",
            ))

        incompat = re.search(
            r'Incompatible mods:\s*(\[list\].*?\[/list\])',
            body,
            re.DOTALL | re.IGNORECASE,
        )

        if re.search(r'Incompatible mods:', body, re.IGNORECASE) and incompat is None:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Incompatible mods block has no BBCode list",
                context="The incompatible-mod list is a heading sentence followed by a [list]",
            ))
        elif incompat is not None:
            block = incompat.group(1)

            if not re.search(r'\[\*\]\s*\S', block):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    "Incompatible mods block has a vacant list",
                    context="Emit one [*] item per known incompatible mod, or omit the block",
                ))

        if re.search(r'compatible with any other mods', body, re.IGNORECASE):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Compatibility section carries the removed multi-mod claim",
                context="List known incompatible mods instead, or omit the block entirely",
            ))

        if re.search(r'actively tested \(and developed\)', body, re.IGNORECASE):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Compatibility section carries the removed development-platform paragraph",
                context="The development-and-testing paragraph was removed from the template",
            ))

        if re.search(r'\[h1\]\s*Load Order\s*\[/h1\]', body, re.IGNORECASE):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Load Order is a top-level section",
                context="Load Order is the [h2]Load Order[/h2] subsection of Compatibility",
            ))

        malformed_url = re.search(r'\[ul=', body, re.IGNORECASE)

        if malformed_url:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Malformed link tag: [ul=...] must be [url=...]",
                context="BBCode links use [url=<TARGET>]text[/url]",
            ))

    def _check_related_mods(self, content: str):
        """Check the conditional Related Mods section and its link priority."""
        body = self._extract_section_body(content, RELATED_MODS_HEADING)

        if body is None:
            return

        if not re.search(r'\[list\]', body, re.IGNORECASE):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Related Mods section has no BBCode list",
                context="Related Mods is a heading followed by one [*] item per mod",
            ))
            return

        if not re.search(r'\[\*\]\s*\S', body):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Related Mods section has a vacant list",
                context="Emit one [*] item per evidenced related mod",
            ))

        for target in re.findall(r'\[url=([^\]]+)\]', body):
            if target.startswith(STEAM_URL_PREFIX):
                if not target.startswith(
                    "https://steamcommunity.com/sharedfiles/filedetails/?id="
                ):
                    self.issues.append(ValidationIssue(
                        ValidationSeverity.ERROR,
                        f"Steam-hosted related mod link has an unexpected target: {target}",
                        context="A Steam link must point at the mod's Workshop page",
                    ))
                continue

            if not target.startswith(LINK_FILTER_PREFIX):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Related mod link is not link-filtered: {target}",
                    context=f"Non-Steam related mod links must use {LINK_FILTER_PREFIX}<TARGET>",
                ))
                continue

            filtered = target[len(LINK_FILTER_PREFIX):]

            if not (
                filtered.startswith("https://nexusmods.com/")
                or filtered.startswith("https://www.nexusmods.com/")
                or filtered.startswith("https://github.com/")
            ):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Related mod link does not use the documented priority: {filtered}",
                    context="Use the mod's Steam Workshop page, otherwise its Nexus Mods "
                            "page, otherwise its GitHub repository",
                ))

    def _check_contributing_section(self, content: str):
        """Check that Contributing carries only the fixed guidelines sentence."""
        body = self._extract_section_body(content, "Contributing")

        if body is None:
            return

        if not body.strip():
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Contributing section has no content",
                context="Emit the fixed guidelines sentence, or omit the section with "
                        "its heading and directive comment",
            ))
            return

        if re.search(
            r'You are welcome to submit any suggestion', body, re.IGNORECASE
        ):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Contributing section carries the removed welcome paragraph",
                context="The section carries only the fixed guidelines sentence",
            ))

        if re.search(re.escape(SUPERSEDED_CONTRIBUTING_SENTENCE), body):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Contributing section carries the removed contributions-managed sentence",
                context="It was removed from the template contract",
            ))

        if re.search(re.escape(SUPERSEDED_CONTRIBUTING_ISSUE_SENTENCE), body):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Contributing section carries the removed issue-tracker sentence",
                context="It was removed from the template contract",
            ))

        if not re.search(r'\]Contributing Guidelines\[/url\]', body):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Contributing section is missing the fixed guidelines sentence",
                context="Use: " + CONTRIBUTING_FIXED_SENTENCE,
            ))

    def _check_troubleshooting_sentence(self, content: str):
        """Check the conditional troubleshooting document sentence."""
        body = self._extract_section_body(content, "Support")

        if body is None:
            return

        if "[[TROUBLESHOOTING" in content or "[[ADDITIONAL_SUPPORT]]" in content:
            return

        mentions_guide = re.search(r'\]Troubleshooting Guide\[/url\]', body)

        if mentions_guide and not re.search(re.escape(TROUBLESHOOTING_FIXED_SENTENCE), body):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Troubleshooting sentence does not match the fixed wording",
                context="Expected: See the [url=<TROUBLESHOOTING_URL>]Troubleshooting "
                        "Guide[/url] for diagnostic procedures and resolutions to "
                        "recurring problems.",
            ))
    def _check_project_engagement(self, content: str):
        """Check the fixed Project Engagement links.

        The line carries placeholders, so the fixed-line comparison skips it;
        this check covers its link placement explicitly: GitHub is linked to the
        repository, and the Steam Workshop is plain text.
        """
        body = self._extract_section_body(content, "Project Engagement")

        if body is None:
            return

        if not re.search(r'\]GitHub\[/url\]', body):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Project Engagement does not link GitHub to the repository",
                context="Use [url=<REPOSITORY_URL>]GitHub[/url]",
            ))

        if re.search(
            r'\[url=[^\]]*steamcommunity\.com/sharedfiles/filedetails/[^\]]*\]'
            r'Steam Workshop\[/url\]',
            body,
            re.IGNORECASE,
        ):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Project Engagement links the Steam Workshop",
                context="The Steam Workshop in this line is plain text",
            ))

        if not re.search(r'favourite on the Steam Workshop!', body):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Project Engagement does not end with the fixed Steam Workshop clause",
                context="Use: or upvoting it and adding it as a favourite on the "
                        "Steam Workshop!",
            ))

    def _check_license_section(self, content: str):
        """Check the fixed License sentence and its linked licence title.

        The License line carries placeholders, so the fixed-line comparison skips
        it; this check covers its structure explicitly.
        """
        body = self._extract_section_body(content, "License")

        if body is None:
            return

        expected = re.search(
            r'This mod is distributed under the '
            r'\[url=[^\]]+\][^\]]+\[/url\][^.]*\.',
            body,
        )

        if expected is None:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "License sentence is not the fixed form",
                context="Expected: This mod is distributed under the "
                        "[url=<LICENSE_URL>]<LICENCE>[/url]<suffix>.",
            ))

        if re.search(r'for additional information', body, re.IGNORECASE):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "License section carries the removed additional-information sentence",
                context="The licence title itself links to LICENSE; no separate sentence is used",
            ))

        if re.search(r'\]\s*\[url=', body):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "License section carries a separate LICENSE link",
                context="Integrate the URL into the licence title instead",
            ))

    def _extract_section_body(self, content: str, section: str) -> Optional[str]:
        """Return the text between a given [h1] section heading and the next one."""
        match = re.search(
            rf'\[h1\]\s*{re.escape(section)}\s*\[/h1\](.*?)(?=\[h1\]|\Z)',
            content,
            re.IGNORECASE | re.DOTALL,
        )

        return match.group(1) if match else None

    def _check_installation_badges(self, content: str):
        """Check the installation badge block and its line layout."""
        body = self._extract_section_body(content, "Installation")

        if body is None:
            return

        badges = BADGE_PATTERN.findall(body)

        if not badges:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Installation section has no store badge",
                context=f"Every badge must use {BADGE_STORE_PREFIX}<store>.png",
            ))
            return

        for target, store in badges:
            if target.startswith(STEAM_URL_PREFIX):
                if not target.startswith(
                    "https://steamcommunity.com/sharedfiles/filedetails/?id="
                ):
                    self.issues.append(ValidationIssue(
                        ValidationSeverity.ERROR,
                        f"Steam-hosted badge has an unexpected target: {target}",
                        context="A Steam-hosted badge must link to "
                                "https://steamcommunity.com/sharedfiles/filedetails/?id=<id>",
                    ))
                continue

            if not target.startswith(LINK_FILTER_PREFIX):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Non-Steam badge target is not link-filtered: {target}",
                    context=f"Every non-Steam badge must use {LINK_FILTER_PREFIX}<TARGET>",
                ))

        for index, line in enumerate(body.splitlines()):
            if not BADGE_PATTERN.search(line):
                continue

            count = len(BADGE_PATTERN.findall(line))

            if count > MAX_BADGES_PER_LINE:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Installation badge line carries {count} badges; the maximum is "
                    f"{MAX_BADGES_PER_LINE}",
                    line_number=index + 1,
                    context="Split the badges so that no line exceeds three",
                ))

            if not line.startswith(BADGE_LINE_PREFIX):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    "Installation badge line is missing its four-space prefix",
                    line_number=index + 1,
                    context="Every badge line begins with exactly four spaces",
                ))

            stripped = line[len(BADGE_LINE_PREFIX):] if line.startswith(BADGE_LINE_PREFIX) else line.strip()
            residue = BADGE_PATTERN.sub("", stripped).strip()

            if residue:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Installation badge line carries unexpected content: {residue}",
                    line_number=index + 1,
                    context="Badges on one line are separated by exactly one space",
                ))

        badge_lines = [
            (index, line)
            for index, line in enumerate(body.splitlines())
            if BADGE_PATTERN.search(line)
        ]

        actual_layout = [len(BADGE_PATTERN.findall(line)) for _, line in badge_lines]
        expected_layout = _balanced_badge_layout(len(badges))

        if actual_layout != expected_layout:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Installation badges are not evenly distributed across lines: got "
                f"{actual_layout}, expected {expected_layout}",
                context="Badges fill each line up to three, then balance evenly, so "
                        "three fill one line and four are laid out two per line",
            ))

        for position, (index, line) in enumerate(badge_lines):
            is_last = position == len(badge_lines) - 1

            if is_last:
                if line.endswith("  "):
                    self.issues.append(ValidationIssue(
                        ValidationSeverity.ERROR,
                        "Final installation badge line has more than one trailing space",
                        line_number=index + 1,
                        context="A badge line ends with at most one space",
                    ))
                continue

            if not line.endswith(" "):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    "Installation badge line is missing its trailing space",
                    line_number=index + 1,
                    context="Every badge line but the last ends with exactly one space",
                ))
            elif line.endswith("  "):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    "Installation badge line has more than one trailing space",
                    line_number=index + 1,
                    context="Every badge line but the last ends with exactly one space",
                ))

        for match in BADGE_PATH_PATTERN.finditer(body):
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Store badge uses an unexpected asset path: {match.group(0)}",
                context=f"All store badges must use {BADGE_STORE_PREFIX}",
            ))

    def _check_link_filtering(self, content: str):
        """Check that no external link bypasses or corrupts the Steam link filter."""
        for index, line in enumerate(content.splitlines()):
            for url in re.findall(r'\[url=([^\]]+)\]', line):
                if "[[ " in url or "[[" in url:
                    # An unresolved placeholder target is reported separately by the
                    # placeholder check, so it is not also a link-filter violation.
                    continue

                if url.startswith(STEAM_URL_PREFIX):
                    continue

                if not url.startswith(LINK_FILTER_PREFIX):
                    self.issues.append(ValidationIssue(
                        ValidationSeverity.ERROR,
                        f"External link is not wrapped in the Steam link filter: {url}",
                        line_number=index + 1,
                        context=f"Every outbound link must use {LINK_FILTER_PREFIX}<TARGET>",
                    ))
                    continue

                target = url[len(LINK_FILTER_PREFIX):]

                if not target.strip():
                    self.issues.append(ValidationIssue(
                        ValidationSeverity.ERROR,
                        "Link filter target is empty",
                        line_number=index + 1,
                        context=f"Append the target URL after {LINK_FILTER_PREFIX}",
                    ))

        for index, line in enumerate(content.splitlines()):
            if re.search(r'\[url=[^\]]*steamcommunity\.com:(?!/linkfilter/\?url=)', line):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    "Link filter prefix was normalised or corrupted",
                    line_number=index + 1,
                    context=f"Use the exact prefix {LINK_FILTER_PREFIX}",
                ))

            if re.search(r'\[url=[^\]]*steamcommunity\.com/linkfilter/', line):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    "Link filter is missing the literal ':/' segment",
                    line_number=index + 1,
                    context=f"Use the exact prefix {LINK_FILTER_PREFIX}",
                ))

    def _check_bbcode_only(self, content: str):
        """Check that the description contains no Markdown or raw HTML."""
        for index, line in enumerate(content.splitlines()):
            if MARKDOWN_PATTERN.search(line):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    "Markdown syntax found in a BBCode description",
                    line_number=index + 1,
                    context="Use BBCode tags only; Steam Workshop does not render Markdown",
                ))

            if RAW_HTML_PATTERN.search(line):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    "Raw HTML found in a BBCode description",
                    line_number=index + 1,
                    context="Use BBCode tags only; raw HTML must not be used",
                ))

    def _check_hidden_text(self, content: str):
        """Check for hidden text and keyword-stuffing techniques."""
        for index, line in enumerate(content.splitlines()):
            if HIDDEN_TEXT_PATTERN.search(line):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    "Hidden text technique found",
                    line_number=index + 1,
                    context="Hidden or transparent text violates Steam Workshop rules",
                ))

    def _check_bracket_balance(self, content: str):
        """Check that BBCode opening and closing tags are balanced."""
        for tag in ("b", "i", "u", "url", "img", "h1", "h2", "h3", "quote", "code"):
            opening = len(re.findall(rf'\[{tag}(?:=[^\]]*)?\]', content, re.IGNORECASE))
            closing = len(re.findall(rf'\[/{tag}\]', content, re.IGNORECASE))

            if opening != closing:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Unbalanced BBCode tag: [{tag}] opened {opening} time(s), closed {closing} time(s)",
                    context="Every BBCode opening tag needs a matching closing tag",
                ))


def _check_output_path(repo_root: Path, generated_path: Path) -> List[ValidationIssue]:
    """Check that the description sits at `description/steam-workshop.bbcode`.

    The canonical location is `description/steam-workshop.bbcode` relative to the
    repository root. A path outside the repository, a different directory, or a
    different file name is an error, because consumers locate the description by
    that exact path.
    """
    issues: List[ValidationIssue] = []

    try:
        resolved_root = repo_root.resolve()
        resolved_path = generated_path.resolve()
        relative = resolved_path.relative_to(resolved_root)
    except ValueError:
        issues.append(ValidationIssue(
            ValidationSeverity.ERROR,
            f"Description is outside the repository: {generated_path}",
            context=f"Write the description to {OUTPUT_RELATIVE_PATH} under the repository root",
        ))
        return issues

    expected = Path(OUTPUT_RELATIVE_PATH)

    if relative != expected:
        issues.append(ValidationIssue(
            ValidationSeverity.ERROR,
            f"Description is at the wrong path: {relative}",
            context=f"The canonical output path is {OUTPUT_RELATIVE_PATH}",
        ))

    return issues


def main():
    args = sys.argv[1:]
    force = os.environ.get("STEAM_WORKSHOP_FORCE_FIDELITY", "").strip().lower() in {"1", "true", "yes"}

    while args and args[0].startswith("--"):
        if args[0] in ("--force", "--use-template"):
            force = True
            args = args[1:]
        else:
            break

    if not args:
        print("Usage: validate_steam_workshop_page.py [--force] <repo_root> [generated_file]")
        print(f"  generated_file: the description, normally {OUTPUT_RELATIVE_PATH} under repo_root")
        print("  If generated_file is not provided, reads from stdin (the output-path check is skipped)")
        print("  --force: enforce template fidelity regardless of repository ownership")
        sys.exit(2)

    repo_root = Path(args[0])

    if len(args) > 1:
        generated_path = Path(args[1])
        generated_content = generated_path.read_text(encoding='utf-8')
        path_issues = _check_output_path(repo_root, generated_path)
    else:
        generated_content = sys.stdin.read()
        path_issues = []

    validator = SteamWorkshopPageValidator(repo_root, force=force)
    issues = validator.validate(generated_content)
    issues.extend(path_issues)

    errors = [i for i in issues if i.severity == ValidationSeverity.ERROR]
    warnings = [i for i in issues if i.severity == ValidationSeverity.WARNING]

    if errors:
        print(f"VALIDATION FAILED: {len(errors)} errors, {len(warnings)} warnings")
        for issue in errors:
            print(f"  ERROR: {issue.message}")
            if issue.context:
                print(f"    Context: {issue.context}")
        sys.exit(1)

    if not validator._should_enforce_fidelity():
        print("i  Template fidelity enforcement skipped: repository is not a personal "
              "repository owned by the current git user. Pass --force (or set "
              "STEAM_WORKSHOP_FORCE_FIDELITY=1) when the template is explicitly requested.")
        sys.exit(3)

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