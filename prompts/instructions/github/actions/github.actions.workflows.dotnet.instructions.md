---
description: "Use when creating or revising the .NET GitHub Actions workflow file. Provides the canonical template for dotnet.yml."
applyTo: ".github/workflows/dotnet.yml"
---

Use this exact workflow template for `dotnet.yml`.

The template must remain exactly as written, with only these exceptions:

- `dotnet-version` must be set to the actual .NET version used in the repository.
- If the project uses MonoGame, add the MonoGame setup steps exactly as shown below, immediately before `Restore dependencies`.

```yaml
name: .NET

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  build:
    name: Build
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v7

    - name: Setup .NET
      uses: actions/setup-dotnet@v5
      with:
        dotnet-version: [[REPOSITORY_DOTNET_VERSION]].x

    # Only include this step if the project uses MonoGame. Otherwise, remove it.
    - name: Setup MGCB
      run: |
        dotnet tool install --global dotnet-mgcb
        ln -s ~/.dotnet/tools/mgcb ~/.dotnet/tools/dotnet-mgcb

    # Only include this step if the project uses MonoGame. Otherwise, remove it.
    - name: Setup fonts
      run: |
        echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | sudo debconf-set-selections
        sudo apt install ttf-mscorefonts-installer
        sudo fc-cache -f

    - name: Restore dependencies
      run: dotnet restore

    - name: Build
      run: dotnet build --no-restore

    - name: Test
      run: dotnet test --no-build --verbosity normal
```
