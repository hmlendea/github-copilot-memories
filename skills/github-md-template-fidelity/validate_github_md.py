#!/usr/bin/env python3
"""
GitHub MD Template Fidelity Validator
Validates generated GitHub markdown files against templates and rules for 100% fidelity.
"""

import re
import sys
from pathlib import Path
from typing import List, Optional, Set
from dataclasses import dataclass
from enum import Enum

CONDITIONAL_DIRECTIVE_PATTERN = re.compile(
    r'^\s*<!--\s*(?:Only if|Only when|Include when|Include if|Only for|Always include)\b[^>]*-->',
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
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.skill_dir = Path(__file__).resolve().parent
        self.templates_dir = self.skill_dir / "templates"
        self.rules_dir = self.skill_dir / "rules"
        self.issues: List[ValidationIssue] = []

    def validate(self, target_file: str, generated_content: str) -> List[ValidationIssue]:
        """Validate generated content against template and rules."""
        self.issues = []

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
        self._check_toc_no_emojis(generated_content)
        self._check_mandatory_headings(generated_content, template_content)
        self._check_empty_sections(generated_content)
        self._check_fixed_prose_integrity(generated_content, template_content)

        return self.issues

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

    def _check_toc_no_emojis(self, content: str):
        """Check Table of Contents has no emojis in entries."""
        # Find ToC section
        toc_match = re.search(r'##\s*📑\s*Table of Contents\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if not toc_match:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                "Table of Contents section missing",
                context="Required ToC section not found"
            ))
            return

        toc_content = toc_match.group(1)
        # Check for emojis in ToC entries (links)
        toc_entries = re.findall(r'\[([^\]]+)\]\(#[^\)]+\)', toc_content)
        for entry in toc_entries:
            # Check for emoji characters
            if re.search(r'[\U0001F300-\U0001F9FF]', entry):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Emoji found in ToC entry: {entry}",
                    context="Table of Contents must not contain emojis in entry text"
                ))

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

        Conditional blocks may legitimately be omitted, so they are excluded from
        comparison. Lines carrying placeholders or inline conditional directives are
        not fixed prose either and are skipped.
        """
        template_lines = self._strip_front_matter(template_content).splitlines()
        gated_indices = self._get_conditional_indices(template_lines)
        document_prose = self._normalise_prose(content)
        body_start = self._get_body_start_index(template_lines)
        in_code_block = False

        for index in range(body_start, len(template_lines)):
            template_line = template_lines[index]
            stripped = template_line.strip()

            if stripped.startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block or index in gated_indices:
                continue

            prose = self._normalise_prose(template_line)

            if not self._is_fixed_prose(template_line, prose):
                continue

            if prose not in document_prose:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Fixed template prose changed or missing: {prose}",
                    line_number=index + 1,
                    context="Only placeholders and HTML comments may be changed"
                ))

    @staticmethod
    def _get_body_start_index(template_lines: List[str]) -> int:
        """Return the index of the first document heading, skipping template prose."""
        for index, template_line in enumerate(template_lines):
            if HEADING_PATTERN.match(template_line.strip()):
                return index

        return 0

    @staticmethod
    def _is_fixed_prose(template_line: str, prose: str) -> bool:
        """Report whether a template line is comparable fixed prose."""
        if not prose:
            return False

        if CONDITIONAL_DIRECTIVE_PATTERN.search(template_line):
            return False

        if PLACEHOLDER_PATTERN.search(template_line):
            return False

        if HEADING_PATTERN.match(prose):
            return True

        if prose.startswith('|'):
            return False

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
    def _get_conditional_indices(template_lines: List[str]) -> Set[int]:
        """Return template line indices governed by a conditional directive."""
        gated_indices: Set[int] = set()

        for index, template_line in enumerate(template_lines):
            if not CONDITIONAL_DIRECTIVE_PATTERN.search(template_line):
                continue

            if re.sub(r'<!--.*?-->', '', template_line, flags=re.DOTALL).strip():
                continue

            block_start = None

            for offset in range(index + 1, len(template_lines)):
                if template_lines[offset].strip():
                    block_start = offset
                    break

            if block_start is None:
                continue

            heading_match = HEADING_PATTERN.match(template_lines[block_start].strip())

            if heading_match is None:
                for offset in range(block_start, len(template_lines)):
                    if offset > block_start and HEADING_PATTERN.match(template_lines[offset].strip()):
                        break

                    gated_indices.add(offset)

                continue

            heading_level = len(heading_match.group(1))

            for offset in range(block_start, len(template_lines)):
                nested_match = HEADING_PATTERN.match(template_lines[offset].strip())

                if offset > block_start and nested_match and len(nested_match.group(1)) <= heading_level:
                    break

                gated_indices.add(offset)

        for index, template_line in enumerate(template_lines):
            if index in gated_indices or not HEADING_PATTERN.match(template_line.strip()):
                continue

            for offset in range(index + 1, len(template_lines)):
                if not template_lines[offset].strip():
                    continue

                if CONDITIONAL_DIRECTIVE_PATTERN.search(template_lines[offset]):
                    gated_indices.add(index)

                break

        return gated_indices

    @staticmethod
    def _remove_html_comments(content: str) -> str:
        """Remove template comments before comparing generated prose."""
        return re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)


def main():
    if len(sys.argv) < 3:
        print("Usage: validate_github_md.py <repo_root> <target_file> [generated_file]")
        print("  If generated_file not provided, reads from stdin")
        sys.exit(1)

    repo_root = Path(sys.argv[1])
    target_file = sys.argv[2]

    if len(sys.argv) > 3:
        generated_content = Path(sys.argv[3]).read_text(encoding='utf-8')
    else:
        generated_content = sys.stdin.read()

    validator = GitHubMDValidator(repo_root)
    issues = validator.validate(target_file, generated_content)

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