# Security Policy

This policy describes how security concerns for the GitHub Copilot Memories repository are reported and handled. The repository publishes instruction files, skills, and agents for GitHub Copilot Chat and OpenAI Codex; it does not distribute executable software, host services, or process user data.

## 📑 Table of Contents

- [Supported Versions](#supported-versions)
- [Reporting a Vulnerability](#reporting-a-vulnerability)
- [Scope](#scope)
- [Disclosure Policy](#disclosure-policy)
- [Safe Harbour](#safe-harbour)
- [Recognition](#recognition)

## 🛡️ Supported Versions

Use this table to indicate which project versions currently receive security maintenance.

| Version | Distribution Channel | Supported |
|---------|--------------------|-----------|
| Latest version | GitHub repository | ✅ |
| Preceding versions | Any distribution channel | ❌ |

## 🚨 Reporting a Vulnerability

Please do not disclose suspected vulnerabilities publicly before maintainers have had an opportunity to validate and remediate them.

To report a vulnerability:
- [GitHub Security Advisories](https://github.com/hmlendea/github-copilot-memories/security/advisories)
- Contact the maintainers directly

## 📌 Scope

The subsequent report categories are in scope for this repository:
- Malicious or misleading instruction files, skills, or agents that could compromise user environments
- Insecure hook scripts that execute arbitrary code during Copilot or Codex sessions
- Credential, secret, or personal-data exposure in repository content

The subsequent categories are out of scope unless explicitly stated to the contrary:
- Vulnerabilities in third-party software referenced by instructions
- Issues in external services or platforms (GitHub, VS Code, Codex)
- Typos, documentation errors, or non-security-related bugs

## 📢 Disclosure Policy

This project follows coordinated disclosure:
1. Vulnerabilities are investigated privately.
2. A remediation plan is prepared and validated.
3. Public disclosure is published after a fix, mitigation, or agreed risk decision is available.
4. Credit is attributed in accordance with reporter preference and project policy.

## 🧾 Safe Harbour

If your research is conducted in good faith, confined to authorised scope, and disclosed responsibly, the maintainers will not pursue action for policy-compliant activity.

## 🙏 Recognition

We appreciate responsible disclosure. Reporters who desire public attribution may be acknowledged in release notes, advisories, or a dedicated acknowledgements section.