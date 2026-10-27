---
description: "Use for C# architecture and fitness tests. Covers ArchUnit.NET, project placement, boundaries, dependency rules, and protection against unrequested modifications."
applyTo: "**/*.ArchitectureTests.csproj,**/*.ArchitectureTests/**/*.cs"
---
## C#

### Architecture/Fitness Tests
- Fitness and architecture tests MUST live in a project named `<RootNamespace>.ArchitectureTests`.
- Fitness and architecture tests MUST use ArchUnit.NET and NUnit.
- Architecture/Fitness tests MUST NEVER be modified by the agent, even if they are failing, unless the user EXPLICITLY asks for it.
- Architecture tests MUST explicitly load all relevant production assemblies, exclude test assemblies, and reuse the loaded architecture for the test run.
- Every rule MUST select expected types; tests MUST fail when a selector matches none rather than pass vacuously.
- Tests MUST enforce the documented layer dependency matrix. Domain MUST NOT depend on Application, Infrastructure, or API; Application MUST NOT depend on Infrastructure or API; Infrastructure MUST NOT depend on API; and API MUST NOT reference Domain directly.
- Dependency rules MUST be checked independently at both levels: type dependencies in the loaded production assemblies and project/assembly references declared by the production projects. A passing type-dependency check MUST NOT substitute for the project/assembly-reference check.
- API boundary rules MUST verify that API code does not directly depend on Entity Framework, DynamoDB, or their persistence namespaces. API MUST NOT contain public repositories or command/query handlers; controllers, request/response contracts, and validation contracts MUST use the prescribed API namespaces; and controllers MUST NOT depend on repositories.
- Application boundary and placement rules MUST verify that Application does not depend on persistence implementations, DynamoDB, or Entity Framework, and does not expose controllers or middleware. Repository and service interfaces, commands, queries, and their handlers MUST be placed in their designated namespaces. Validators MUST be placed in the matching command or query use-case namespace.
- Domain boundary rules MUST verify that Domain does not depend on ASP.NET Core, Entity Framework, DynamoDB, Dapper, or MediatR. Domain types MUST NOT use persistence attributes. Public controllers, handlers, DTOs, validation contracts, commands, queries, and repositories MUST be prohibited in Domain.
- Architecture tests MUST verify that production code projects do not declare `InternalsVisibleTo`.
- Tests MUST check cycles where components are defined as independent or acyclic. Do not assume layer names or impose a layered design beyond the documented matrix. Any permitted cycle MUST be documented and narrowly scoped.
- Enforce namespace placement, naming, and interface implementation conventions only when required by the documented architecture; do not duplicate generic style or analyser rules.
- Failure messages MUST identify the violated boundary and reason. Rule exceptions MUST be explicit and narrowly scoped.
- Architecture tests are exempt from the business-unit-test assertion requirement.