---
description: "Use when creating or revising the Steam Workshop GitHub Actions workflow file. Provides the canonical template for steam-workshop.yml."
applyTo: ".github/workflows/steam-workshop.yml"
---

Use this exact workflow template for steam-workshop.yml.

```yaml
name: Steam Workshop

on:
  push:
    tags:
    - 'v*.*.*'

jobs:
  release:
    name: Release
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v7

    - name: Download the release asset
      run: |
        wget "https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/releases/download/${{github.ref_name}}/[[RELEASE_ASSET_LABEL]]_${GITHUB_REF:11}.zip" -O "release.zip"
        unzip "release.zip" -d "release/"

    - name: Upload
      uses: hmlendea/steam-workshop-update@v1.0.0
      with:
        appid: [[STEAM_APP_ID]]
        itemid: [[STEAM_WORKSHOP_ITEM_ID]]
        path: "release/[[RELEASE_ASSET_LABEL]]/"
        changenote: "[url=https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/releases/tag/${{github.ref_name}}]Version ${{github.ref_name}}[/url]"
      env:
        STEAM_USERNAME: ${{secrets.STEAM_USERNAME}}
        STEAM_PASSWORD: ${{secrets.STEAM_PASSWORD}}
        STEAM_2FASEED: ${{secrets.STEAM_2FA_SEED}}
```
