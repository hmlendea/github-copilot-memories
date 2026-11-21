---
description: "Use when investigating, inspecting, or considering decompilation of hmlendea-owned NuGet packages, when locating their versioned GitHub documentation, or when writing C# HTTP or network code in an hmlendea repository. Obligates the `csharp-nuget-usage` skill."
applyTo: "**/*.{cs,csproj}"
---

## Mandatory Skill

Every use of an `hmlendea`-owned NuGet package, and all HTTP and network utility code in an `hmlendea`-owned repository, is governed by the `csharp-nuget-usage` skill. Invoking that skill is mandatory, not optional: read `skills/csharp-nuget-usage/SKILL.md` before inspecting such a package or writing such code, and apply it in full.

The skill holds the versioned documentation lookup procedure, the prohibition on investigating by decompilation, the `NuciWeb.HTTP` requirement, and the prescribed `HttpClientCreator`, `UserAgentFetcher`, `NetworkUtils`, and Kestrel IPv6 call rules.
