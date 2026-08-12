---
description: "Use when creating or revising the Nexus Mods GitHub Actions workflow file. Provides the canonical template for nexus-mods.yml."
applyTo: ".github/workflows/nexus-mods.yml"
---

Use this exact workflow template for nexus-mods.yml.

```yaml
name: Nexus Mods

on:
  push:
    tags:
    - 'v*.*.*'
  workflow_dispatch:
    inputs:
      tag:
        description: 'Tag to release'
        required: true

jobs:
  release:
    name: Release
    runs-on: ubuntu-latest

    env:
      VERSION: ${{ inputs.tag || github.ref_name }}

    steps:
    - uses: actions/checkout@v7

    - name: Download the release asset
      run: |
        RELEASE_ASSET_NAME="[[RELEASE_ASSET_LABEL]]_${VERSION#v}.zip"
        wget "https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/releases/download/${VERSION}/${RELEASE_ASSET_NAME}" -O "release.zip"

    - name: Upload
      uses: Nexus-Mods/upload-action@v1.0.0-beta.10
      with:
        api_key: ${{ secrets.NEXUSMODS_API_KEY }}
        file_id: [[NEXUSMODS_FILE_ID]]
        filename: release.zip
        display_name: [[RELEASE_ASSET_LABEL]].zip
        version: ${{env.VERSION}}
        description: "Changelog: https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/releases/${{env.VERSION}}"
        category: main
        archive_existing_version: true
        update_mod_version: true
```
