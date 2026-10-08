---
description: "Template for CONTRIBUTING.md files."
applyTo: "CONTRIBUTING.md"
---
This is the `CONTRIBUTING.md` template that must be used.
---

# Contributing to [[PROJECT_TITLE]]

This document covers the guidelines and processes for contributing to this project, including how to report issues, suggest enhancements, submit code changes, and follow project standards.

## 📑 Table of Contents

<!-- Generate one entry per `##`, `###`, and `####` heading present in the final output, in order. Indent each level by two spaces. Use the text and anchor without heading emojis. -->

## 🤝 How to Contribute

### Reporting Issues

<!-- Only if the repository uses GitHub Issues. -->
- Search existing issues first.
- Use the issue templates if available.
- Provide clear reproduction steps.
- Include environment details.

### Suggesting Enhancements

<!-- Only if the repository accepts feature requests. -->
- Check the roadmap and existing discussions.
- Explain the use case and expected behavior.
- Consider implementation complexity.

### Code Contributions

#### Prerequisites

<!-- Only if specific prerequisites exist. -->
- [[PREREQUISITES]]

#### Development Setup

<!-- Always include. Replace with project-native commands. -->
```bash
# Clone the repository
git clone https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]].git
cd [[GITHUB_REPO_NAME]]

# Install dependencies
[[DEVELOPMENT_SETUP]]
```

#### Making Changes

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes.
4. Run tests: `[[TEST_COMMAND]]` <!-- Only if tests exist. -->
5. Run linters: `[[LINT_COMMAND]]` <!-- Only if linters exist. -->
6. Commit with clear and descriptive messages.
7. Push to your fork.
8. Open a Pull Request.

#### Pull Request Guidelines

- Target the `[[DEFAULT_BRANCH]]` branch.
- Keep PRs focused and atomic.
- Update documentation if applicable.
- Add tests for any new functionality.
- Ensure the CI checks pass.

### Code Style

<!-- Only if a style guide or linter config exists. -->
Follow the project's coding standards:
- [[CODE_STYLE_GUIDE]]
- Run `[[FORMAT_COMMAND]]` before committing.

### Testing

<!-- Only if tests exist. -->
```bash
# Run all tests
[[TEST_COMMAND]]

# Run specific test suite
[[TEST_SPECIFIC_COMMAND]]
```

### Documentation

<!-- Only if documentation exists or is generated. -->
- Update relevant docs for changes.
- Follow the documentation style guide.
- Preview changes locally if possible.

## 📋 Code of Conduct

<!-- Only if `CODE_OF_CONDUCT.md` exists. -->
This project follows the [[CODE_OF_CONDUCT_DOCUMENT_LINK]].

## 🔒 Security

<!-- Only if `SECURITY.md` exists. -->
Report security vulnerabilities per the [[SECURITY_DOCUMENT_LINK]].

## 📄 License

<!-- Only if `LICENSE` exists. -->
By contributing, you agree that your contributions will be licensed under the [[LICENSE_TITLE]].

## 🙏 Recognition

<!-- Only if a contributors list or recognition mechanism exists. -->
Contributors are recognized in [[RECOGNITION_LOCATION]].

## ❓ Getting Help

<!-- Only if support channels exist. -->
- [[SUPPORT_CHANNELS]]
- Check existing discussions and documentation first.