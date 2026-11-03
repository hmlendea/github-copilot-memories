---
description: "Use for C# integration tests and integration-test projects. Covers project placement, API scenarios, framework, response assertions, and external dependencies."
applyTo: "**/*.IntegrationTests.csproj,**/*.IntegrationTests/**/*.cs"
---
## C#

### Projects
- Integration tests MUST only be written in a dedicated integration-test project, never in a production or unit-test project.
- The default integration-test project name is `[RootNamespace].IntegrationTests`.

### Integration Testing
- API integration tests cover all input/output success and failure scenarios, including applicable HTTP statuses (e.g. 400, 401, 404, 500).
- Use project integration framework; absent framework defaults to NUnit + FluentAssertions + Microsoft.AspNetCore.Mvc.Testing.
- Do not use xunit unless it was explicitly chosen as the project testing framework or already in use.
- Assert response body and status. Parameterise with `[InlineData]`/`[Theory]`; mock external dependencies for deterministic speed.
- Integration tests MUST be cross-platform, environment-agnostic, and machine-agnostic; they MUST run without relying on the host OS, machine name, username, home or current directory, filesystem layout, locale, timezone, clock, installed tools, environment variables, hardware, or developer-local services. Use portable temporary resources, controlled configuration, deterministic data, and isolated or explicitly provisioned dependencies; never silently require a local database, network service, container, or platform-specific executable.