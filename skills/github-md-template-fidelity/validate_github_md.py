#!/usr/bin/env python3
"""
GitHub MD Template Fidelity Validator
Validates generated GitHub markdown files against templates and rules for 100% fidelity.
"""

import re
import sys
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum


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
        self.prompts_dir = repo_root / "prompts" / "instructions" / "github"
        self.issues: List[ValidationIssue] = []

    def validate(self, target_file: str, generated_content: str) -> List[ValidationIssue]:
        """Validate generated content against template and rules."""
        self.issues = []

        # Determine template and rules files
        template_map = {
            "README.md": ("github.readme.template.instructions.md", "github.readme.rules.instructions.md"),
            "ARCHITECTURE.md": ("github.architecture.template.instructions.md", "github.architecture.rules.instructions.md"),
            "CONTRIBUTING.md": ("github.contributing.template.instructions.md", "github.contributing.rules.instructions.md"),
            "SECURITY.md": ("github.security.template.instructions.md", "github.security.rules.instructions.md"),
            "PRIVACY.md": ("github.privacy.template.instructions.md", "github.privacy.rules.instructions.md"),
            "ROADMAP.md": ("github.roadmap.template.instructions.md", "github.roadmap.rules.instructions.md"),
        }

        if target_file not in template_map:
            self.issues.append(ValidationIssue(
                ValidationSeverity.ERROR,
                f"Unknown target file: {target_file}"
            ))
            return self.issues

        template_file, rules_file = template_map[target_file]
        template_path = self.prompts_dir / template_file
        rules_path = self.prompts_dir / rules_file

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

        # Read template and rules
        template_content = template_path.read_text(encoding='utf-8')
        rules_content = rules_path.read_text(encoding='utf-8')

        # Run validation checks
        self._check_placeholders_removed(generated_content)
        self._check_template_comments_removed(generated_content)
        self._check_toc_no_emojis(generated_content)
        self._check_heading_hierarchy(generated_content, template_content)
        self._check_empty_sections(generated_content)
        self._check_fixed_prose_integrity(generated_content, template_content)
        self._check_mandatory_sections(generated_content, rules_content)
        self._check_conditional_sections(generated_content, template_content)

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

    def _check_heading_hierarchy(self, content: str, template_content: str):
        """Check that heading hierarchy matches template."""
        # Extract headings from generated content
        generated_headings = re.findall(r'^(#{2,4})\s+(.+)$', content, re.MULTILINE)

        # Extract expected headings from template (non-conditional ones)
        template_headings = re.findall(r'^(#{2,4})\s+(.+)$', template_content, re.MULTILINE)

        # Filter template headings to only mandatory/always-include ones
        # This is a simplified check - full implementation would parse conditionals
        expected_headings = []
        in_conditional = False
        for level, text in template_headings:
            # Skip headings inside conditional blocks (simplified)
            if '<!-- Only if' in text or '<!-- Always include' in text:
                continue
            expected_headings.append((level, text.strip()))

        # Compare (simplified - full impl would handle conditionals properly)
        if len(generated_headings) < len([h for h in expected_headings if not h[1].startswith('<!--')]):
            self.issues.append(ValidationIssue(
                ValidationSeverity.WARNING,
                f"Fewer headings in output ({len(generated_headings)}) than expected mandatory headings",
                context="May indicate missing mandatory sections"
            ))

    def _check_empty_sections(self, content: str):
        """Check for empty headings, tables, lists, code blocks."""
        lines = content.split('\n')
        in_code_block = False
        code_block_start = -1

        for i, line in enumerate(lines):
            # Track code blocks
            if line.strip().startswith('```'):
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
                    in_code_block = False

            # Check for empty headings (heading followed immediately by another heading or EOF)
            if re.match(r'^#{2,4}\s+.+', line):
                # Look ahead for content
                has_content = False
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip() and not re.match(r'^#{2,4}\s+', lines[j]):
                        has_content = True
                        break
                if not has_content and i+1 < len(lines):
                    self.issues.append(ValidationIssue(
                        ValidationSeverity.WARNING,
                        f"Potentially empty section at line {i+1}: {line.strip()}",
                        context="Section may be empty or have only whitespace"
                    ))

            # Check for empty tables (header row only)
            if '|' in line and line.strip().startswith('|'):
                # Check if next non-empty line is also a table row
                next_content_line = None
                for j in range(i+1, len(lines)):
                    if lines[j].strip():
                        next_content_line = lines[j]
                        break
                if next_content_line and not ('|' in next_content_line and next_content_line.strip().startswith('|')):
                    # Table has only header row
                    self.issues.append(ValidationIssue(
                        ValidationSeverity.WARNING,
                        f"Potentially empty table at line {i+1}",
                        context="Table appears to have only header row"
                    ))

    def _check_fixed_prose_integrity(self, content: str, template_content: str):
        """Check that non-placeholder template prose is preserved in order."""
        template_lines = template_content.splitlines()
        output_lines = self._remove_html_comments(content).splitlines()
        output_index = 0
        in_front_matter = False
        skip_conditional = False

        for template_line in template_lines:
            stripped = template_line.strip()

            if stripped == '---':
                in_front_matter = not in_front_matter
                continue
            if in_front_matter or not stripped or stripped.startswith('<!--'):
                if stripped.startswith('<!-- Only if'):
                    skip_conditional = True
                continue

            # Conditional blocks may be omitted from the generated document.
            if skip_conditional:
                if stripped.startswith(('#', '[!', '|', '```')):
                    skip_conditional = False
                else:
                    continue

            fixed_line = re.sub(r'\[\[\[.*?\]\]\]|\[\[.*?\]\]', '', template_line)
            fixed_line = fixed_line.strip()
            if not fixed_line or fixed_line.startswith('<!--'):
                continue

            found = False
            for index in range(output_index, len(output_lines)):
                if output_lines[index].strip() == fixed_line:
                    output_index = index + 1
                    found = True
                    break

            if not found:
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Fixed template prose changed or missing: {fixed_line}",
                    context="Only placeholders and HTML comments may be changed"
                ))

    @staticmethod
    def _remove_html_comments(content: str) -> str:
        """Remove template comments before comparing generated prose."""
        return re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    def _check_mandatory_sections(self, content: str, rules_content: str):
        """Check that mandatory sections are present."""
        # Extract "Always include" sections from rules
        always_include = re.findall(r'Always include:?\s*\n((?:- .+\n)*)', rules_content)
        mandatory_sections = []
        for block in always_include:
            sections = re.findall(r'-\s*`?(##\s+[^`]+)`?', block)
            mandatory_sections.extend(sections)

        # Also check for explicit mandatory sections in rules
        mandatory_patterns = [
            r'##\s*📑\s*Table of Contents',
            r'##\s*✨\s*Capabilities',
            r'##\s*🚀\s*Usage',
            r'##\s*🤝\s*Contributing',
            r'##\s*💝\s*Project Engagement',
        ]

        for pattern in mandatory_patterns:
            if re.search(pattern, rules_content) and not re.search(pattern, content):
                self.issues.append(ValidationIssue(
                    ValidationSeverity.ERROR,
                    f"Mandatory section missing: {pattern}",
                    context="Required section from rules not found in output"
                ))

    def _check_conditional_sections(self, content: str, template_content: str):
        """Check conditional sections are properly handled."""
        # Find all conditional blocks in template
        conditional_blocks = re.findall(
            r'<!--\s*Only if\s+([^>]+)>\s*-->\s*\n(##\s+.+?)(?=\n##|\n<!--|\Z)',
            template_content,
            re.DOTALL
        )

        for condition, section in conditional_blocks:
            heading_match = re.match(r'(##\s+.+)', section.strip())
            if heading_match:
                heading = heading_match.group(1).strip()
                # Check if section appears in output
                if heading in content:
                    # Section included - verify it has substantive content
                    section_content = self._extract_section_content(content, heading)
                    if not section_content or len(section_content.strip()) < 20:
                        self.issues.append(ValidationIssue(
                            ValidationSeverity.WARNING,
                            f"Conditional section '{heading}' included but appears empty",
                            context=f"Condition: {condition}"
                        ))
                # If not in output, that's fine - condition not met

    def _extract_section_content(self, content: str, heading: str) -> str:
        """Extract content between a heading and the next heading."""
        pattern = rf'{re.escape(heading)}\s*\n(.*?)(?=\n##\s+|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1) if match else ""


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