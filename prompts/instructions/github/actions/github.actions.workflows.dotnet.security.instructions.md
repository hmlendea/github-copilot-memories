---
description: "Use when creating or revising the .NET Security GitHub Actions workflow file. Provides the canonical template for security.yml."
applyTo: ".github/workflows/security.yml"
---

Use this exact workflow template for `security.yml`.

The template must remain exactly as written, with only these exceptions:

- `dotnet-version` must be set to the actual .NET version used in the repository.

The `security-events` permission must be `write`. The CodeQL `analyze` action uploads SARIF results to GitHub Code Scanning, and that upload requires the `security-events: write` scope. With `security-events: read`, the upload fails on `push` and `schedule` runs with `Resource not accessible by integration`, while `pull_request` runs still complete. GitHub's own CodeQL workflow therefore grants `security-events: write`.

```yaml
name: Security

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]
  schedule:
    - cron: '0 0 * * 0'

jobs:
  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read

    steps:
    - uses: actions/checkout@v7

    - name: Setup .NET
      uses: actions/setup-dotnet@v5
      with:
        dotnet-version: [[DOTNET_VERSION]].x

    - name: Restore dependencies
      run: dotnet restore

    - name: Check for vulnerable packages
      run: dotnet list package --vulnerable --include-transitive

    - name: Run CodeQL Analysis
      uses: github/codeql-action/init@v4
      with:
        languages: csharp

    - name: Build
      run: dotnet build --no-restore

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v4
```
