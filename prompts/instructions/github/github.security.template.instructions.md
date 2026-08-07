---
description: "Use when the user inquires regarding revising, creating, or generating a SECURITY.md. Auto-invoked by requests such as 'revise the security policy', 'create a security policy', 'compose the security policy', or 'generate SECURITY.md'. Populates project-specific disclosure scope and supported-version details while applying the standard structure."
applyTo: "SECURITY.md"
---
This is the `SECURITY.md` template that shall be utilised.
---

<!-- BEGIN SECURITY TEMPLATE IMMUTABLE -->

# Security Policy

[[[Brief summary of the policy objective, reporting principles, and supported-release coverage.]]]

## 📑 Table of Contents

<!-- Generate one entry per ##/###/#### heading present in the final output, in order. Do not include emojis here. -->

## 🛡️ Supported Versions

Use this table to indicate which project versions currently receive security maintenance.

| Version | Distribution Method | Supported |
|---------|--------------------|-----------|
| [[Latest version or branch, e.g. 2.x]] | [[Supported distribution method, e.g. GitHub Releases]] | ✅ |
| [[Latest version or branch, e.g. 2.x]] | [[Unsupported distribution method, e.g. GitHub Releases]] | ❌ |
| [[Outdated version or branch, e.g. 1.x]] | [[Supported distribution method, e.g. GitHub Releases]] | ❌ |
| [[Outdated version or branch, e.g. 1.x]] | [[Unsupported distribution method, e.g. GitHub Releases]] | ❌ |

<!-- Add additional rows only when maintainers intentionally support or explicitly deprecate other versions. -->

## 🚨 Reporting a Vulnerability

Please do not disclose suspected vulnerabilities publicly before maintainers have had an opportunity to validate and remediate them.

To report a vulnerability, contact the maintainers directly

## 📌 Scope

The subsequent report categories are in scope for this repository:
- [[In-scope category 1]]
- [[In-scope category 2]]

The subsequent categories are out of scope unless explicitly stated to the contrary:
- [[Out-of-scope category 1]]
- [[Out-of-scope category 2]]

## 📢 Disclosure Policy

This project follows coordinated disclosure:
1. Vulnerabilities are investigated privately.
2. A remediation plan is prepared and validated.
3. Public disclosure is published after a fix, mitigation, or agreed risk decision is available.
4. Credit is attributed in accordance with reporter preference and project policy.

<!-- Only if a safe-harbour statement is available. -->
## 🧾 Safe Harbour

If your research is conducted in good faith, confined to authorised scope, and disclosed responsibly, the maintainers will not pursue action for policy-compliant activity.

<!-- Only if public recognition is practised. -->
## 🙏 Recognition

We appreciate responsible disclosure. Reporters who desire public attribution may be acknowledged in release notes, advisories, or a dedicated acknowledgements section.

<!-- END SECURITY TEMPLATE IMMUTABLE -->
