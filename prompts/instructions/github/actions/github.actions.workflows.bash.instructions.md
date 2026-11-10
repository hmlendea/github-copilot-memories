---
description: "Use when creating or revising the Bash GitHub Actions workflow file. Provides the canonical template for bash.yml."
applyTo: ".github/workflows/bash.yml"
---

Use this exact workflow template for `bash.yml`.

The template must remain exactly as written.

For the full cross-file procedure, including documentation synchronisation and validation, apply the `github-actions-workflow` skill in `skills/github-actions-workflow/SKILL.md`.

```yaml
name: Bash

on:
  push:
    branches:
      - master
  pull_request:
    branches:
      - master
  workflow_dispatch:

permissions:
  contents: read

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v7

      - name: Lint Bash scripts
        shell: bash
        run: |
          shopt -s globstar nullglob
          shellcheck **/*.sh --severity error
```
