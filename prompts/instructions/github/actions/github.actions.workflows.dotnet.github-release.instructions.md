---
description: "Use when creating or revising the GitHub Release workflow for a compilable .NET project. Provides the canonical template for github-release.yml."
applyTo: ".github/workflows/github-release.yml"
---

Use this exact workflow template for `.github/workflows/github-release.yml`.

For the full cross-file procedure, including documentation synchronisation and validation, apply the `github-actions-workflow` skill in `skills/github-actions-workflow/SKILL.md`.

Use this template only for compilable .NET projects, that is, projects that build to release assets. Do not use it for NuGet packages. For a repository that hosts a NuGet package, use `prompts/instructions/github/actions/github.actions.workflows.nuget.github-release.instructions.md` instead.

The template must remain exactly as written, with only the placeholders replaced:

- `[[DOTNET_PROJECT_PATH]]` must be replaced with the repository-relative path of the primary project file whose `TargetFramework` determines the .NET version (for example `NuciCraft.API/NuciCraft.API.csproj`).
- `[[RELEASE_ASSET_GLOB]]` must be replaced with the repository-relative glob of the release assets produced by the release script (for example `NuciCraft.API/bin/Release/nucicraft-api_*`).

```yaml
name: GitHub Release

on:
  release:
    types: [ published ]

permissions:
  contents: write

jobs:
  release:
    name: Build and publish
    runs-on: ubuntu-latest

    steps:
    - name: Check out the repository
      uses: actions/checkout@v7
      with:
        fetch-depth: 0

    - name: Determine the .NET version
      id: dotnet
      run: |
        TARGET_FRAMEWORK="$(sed -n 's|.*<TargetFramework>\(.*\)</TargetFramework>.*|\1|p' [[DOTNET_PROJECT_PATH]] | head -n 1)"

        if [[ -z "${TARGET_FRAMEWORK}" ]]; then
          echo 'ERROR: Could not determine the target framework from [[DOTNET_PROJECT_PATH]].' >&2
          exit 1
        fi

        DOTNET_VERSION="${TARGET_FRAMEWORK#net}"
        echo "version=${DOTNET_VERSION}" >> "$GITHUB_OUTPUT"

    - name: Setup .NET
      uses: actions/setup-dotnet@v5
      with:
        dotnet-version: ${{ steps.dotnet.outputs.version }}.x

    - name: Extract the version from the GitHub tag
      id: version
      run: |
        VERSION="${{ github.event.release.tag_name }}"
        VERSION="${VERSION#v}"
        echo "version=${VERSION}" >> "$GITHUB_OUTPUT"

    - name: Normalise the origin remote URL
      run: git remote set-url origin "https://github.com/${GITHUB_REPOSITORY}.git"

    - name: Build the release artefacts
      env:
        DOTNET_VERSION: ${{ steps.dotnet.outputs.version }}
        RELEASE_VERSION: ${{ steps.version.outputs.version }}
      run: |
        RELEASE_SCRIPT_URL="https://raw.githubusercontent.com/hmlendea/dotnet-release-scripts/refs/heads/master/dotnet/${DOTNET_VERSION}.sh"
        wget --quiet -O - "${RELEASE_SCRIPT_URL}" | bash /dev/stdin "${RELEASE_VERSION}"

    - name: Publish the release assets
      uses: softprops/action-gh-release@v2
      with:
        files: [[RELEASE_ASSET_GLOB]]
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
