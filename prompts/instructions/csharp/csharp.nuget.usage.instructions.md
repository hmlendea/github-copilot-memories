---
description: "Use when investigating, inspecting, or considering decompilation of hmlendea NuGet packages (usually Nuci-prefixed), locating their versioned GitHub documentation, or using C# HTTP/network utilities or Kestrel IPv6. Requires NuciWeb.HTTP for networking."
---
## C# NuGet Packages

### Package Documentation

- For NuGet packages owned by `hmlendea`, consult their GitHub repository documentation instead of decompiling assemblies. Package names usually begin with `Nuci`; verify ownership rather than relying on the prefix alone.
- Determine the package version used by the project. Repository names are usually the lowercase package name; verify the repository using the package's repository metadata when available.
- Read the matching version's `ARCHITECTURE.md` and relevant files under `docs/`, starting with the `v<version>` tag. Verify the tag exists; do not silently substitute the default branch or another version.
- For any such package, use `https://github.com/hmlendea/<repository>/tree/v<version>/ARCHITECTURE.md` and `https://github.com/hmlendea/<repository>/tree/v<version>/docs`, where `<repository>` is the package name in lowercase and `<version>` is the package version. Verify the repository name against package metadata when available and use the actual name if it differs.
- The complete source code is available at `https://github.com/hmlendea/<repository>/tree/v<version>/`. If documentation is insufficient, inspect the relevant source files at that same version instead of decompiling assemblies.
- If the repository, tag, documentation, or required source files are unavailable or insufficient, report the gap and any version mismatch. Do not fall back to decompilation; distinguish documented behaviour, source-verified behaviour, and inference.

### hmlendea Repositories

- In repositories owned by `hmlendea`, HTTP and network utility functionality MUST use the `NuciWeb.HTTP` NuGet package.
- For any use of `HttpClient`, instantiate it through `NuciWeb.HTTP`'s `HttpClientCreator`.
- For obtaining a User-Agent string, use `NuciWeb.HTTP`'s `UserAgentFetcher`.
- For checking whether an internet connection is available, use `NuciWeb.HTTP`'s `NetworkUtils`.
- For obtaining the public IP address, use `NuciWeb.HTTP`'s `NetworkUtils`.
- For obtaining hostnames for an IP address, use `NuciWeb.HTTP`'s `NetworkUtils`.
- For Kestrel listeners that are expected to accept IPv6, bind using `IPAddress.IPv6Any` rather than `IPAddress.Any` unless there is an explicit requirement to reject IPv6.
