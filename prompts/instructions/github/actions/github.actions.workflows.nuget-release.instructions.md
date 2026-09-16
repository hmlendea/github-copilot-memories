---
description: "Use when creating or revising the NuGet.org release workflow for a repository that hosts a NuGet package. Provides the canonical template for nuget-release.yml."
applyTo: ".github/workflows/nuget-release.yml"
---

Use this exact workflow template for `nuget-release.yml`.

The `[[NUGET_PACKAGE_NAME]]` placeholder must be replaced with the NuGet package ID.

The repository must define the `NUGET_USER` secret with the NuGet.org account name associated with the package. NuGet trusted publishing must be configured for the repository so `NuGet/login` can exchange the GitHub Actions OIDC token for a temporary API key.

```yaml
name: NuGet Release

on:
  release:
    types: [ published ]

permissions:
  contents: read

jobs:
  publish:
    name: Publish
    runs-on: ubuntu-latest

    permissions:
      contents: read
      id-token: write

    env:
      NUGET_PACKAGE_NAME: [[NUGET_PACKAGE_NAME]]

    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Setup .NET
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: 10.0.x

    - name: Extract the version from the GitHub tag
      id: version
      run: |
        VERSION="${{ github.ref_name }}"
        VERSION="${VERSION#v}"
        echo "version=$VERSION" >> "$GITHUB_OUTPUT"

    - name: Restore the dependencies
      run: dotnet restore

    - name: Create the NuGet package
      run: dotnet pack -c Release --output ./nupkg -p:Version=${{ steps.version.outputs.version }}

    - name: NuGet login (OIDC to temporary API key)
      uses: NuGet/login@v1
      id: login
      with:
        user: ${{ secrets.NUGET_USER }}

    - name: Publish the NuGet package
      run: dotnet nuget push "./nupkg/${NUGET_PACKAGE_NAME}.${{ steps.version.outputs.version }}.nupkg" --api-key "${{ steps.login.outputs.NUGET_API_KEY }}" --source https://api.nuget.org/v3/index.json --skip-duplicate
```