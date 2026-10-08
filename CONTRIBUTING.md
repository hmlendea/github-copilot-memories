# Contributing to GitHub Copilot Memories

This document covers the guidelines and processes for contributing to this project, including how to report issues, suggest enhancements, submit code changes, and follow project standards.

## 📑 Table of Contents

- [How to Contribute](#-how-to-contribute)
  - [Reporting Issues](#reporting-issues)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Code Contributions](#code-contributions)
    - [Development Setup](#development-setup)
    - [Making Changes](#making-changes)
    - [Pull Request Guidelines](#pull-request-guidelines)
- [Code Style](#-code-style)
- [Documentation](#-documentation)
- [Code of Conduct](#-code-of-conduct)
- [Security Policy](#-security-policy)
- [License](#-license)

## 🤝 How to Contribute

### Reporting Issues

- Search existing issues first.
- Use the issue templates if available.
- Provide clear reproduction steps.
- Include environment details.

### Suggesting Enhancements

- Check the roadmap and existing discussions.
- Explain the use case and expected behavior.
- Consider implementation complexity.

### Code Contributions

#### Development Setup

```bash
# Clone the repository
git clone https://github.com/hmlendea/github-copilot-memories.git
cd github-copilot-memories
```

#### Making Changes

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes.
4. Commit with clear and descriptive messages.
5. Push to your fork.
6. Open a Pull Request.

#### Pull Request Guidelines

- Target the `master` branch.
- Keep PRs focused and atomic.
- Update documentation if applicable.
- Ensure the CI checks pass.

### Code Style

Follow the project's coding standards:
- Instruction files: follow the conventions in `prompts/instructions/common/common.coding.instructions.md`
- Skill files: follow the conventions in `skills/*/SKILL.md`
- Apply British English spelling per `prompts/instructions/language/language.english.instructions.md`

### Documentation

- Update relevant docs for changes.
- Follow the documentation style guide.
- Preview changes locally if possible.

## 📄 License

This project is licensed under the [GNU General Public License v3.0](LICENSE).