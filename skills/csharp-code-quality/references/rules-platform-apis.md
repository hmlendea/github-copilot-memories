# C# Rules: Platform APIs

One directive per C# rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never use `DateTime` or `DateTimeOffset` as an Entity Framework primary key; use an integer or `Guid` key.
- Apply `[OperationContract]` only to methods of `[ServiceContract]` types, and ensure every `[ServiceContract]` declares at least one `[OperationContract]`.
- Declare `[OperationContract(IsOneWay = true)]` methods with a `void` return type.
- Implement `ISerializable` completely: mark the type `[Serializable]`, declare a serialisation constructor, and call `base.GetObjectData` from overrides; derived serialisable types do likewise.
- For each `[OptionalField]` member of a serialisable type, implement an `[OnDeserializing]` or `[OnDeserialized]` method that initialises it.
- Declare serialisation callbacks (`[OnSerializing]`, `[OnSerialized]`, `[OnDeserializing]`, `[OnDeserialized]`) as `private`, non-generic, returning `void`, with a single `StreamingContext` parameter.
- Ensure a class exported via MEF `[Export(typeof(T))]` implements or derives from `T`.
- Mark the Windows Forms `Main` method with `[STAThread]`.
- Ensure every `[ConstructorArgument("name")]` value corresponds to a constructor parameter name.
- Never instantiate a MEF part marked `[PartCreationPolicy(CreationPolicy.Shared)]` with `new`; import it from the container.
- Apply `[PartCreationPolicy]` only to classes also marked `[Export]`.
- Retain no mutable static state in Azure Functions; persist state externally (for example in Durable Entities or storage).
- Never create clients (`HttpClient`, `CosmosClient`, `BlobServiceClient`, and similar) per Azure Functions invocation; reuse them via static fields or dependency injection.
- Never block on asynchronous calls (`.Result`, `.Wait()`, `GetAwaiter().GetResult()`) in Azure Functions; `await` them.
- Restrict durable entity interfaces to methods with at most one parameter returning `void`, `Task`, or `Task<T>`; no generic members, properties, or indexers.
- Use `[SupplyParameterFromQuery]` only with supported types: `bool`, `DateTime`, `decimal`, `double`, `float`, `Guid`, `int`, `long`, `string`, their nullable forms, and arrays of these.
- Apply `[JSInvokable]` only to `public` methods.
- Ensure a Blazor component parameter type corresponds to its route parameter constraint (for example `{id:int}` binds to `int`).
- Use `/` and never `\` in route templates.
- Never start action route templates with `/`, which bypasses the controller route prefix; use `~/` when an absolute route is intentional.
- Bind controller inputs via model binding (`[FromQuery]`, `[FromRoute]`, `[FromBody]`, `[FromHeader]`, `[FromForm]`) instead of reading `Request.Query`, `Request.Form`, `Request.Headers`, or `Request.RouteValues` directly.
- When actions declare route templates, also apply `[Route]` to the controller.
- Never combine unrelated responsibilities in one controller; divide a controller whose actions use disjoint sets of injected dependencies.
- Derive API controllers from `ControllerBase`, not `Controller`, unless they return views.
- Never instantiate `HttpClient` per request or operation; obtain clients from `IHttpClientFactory` (named or typed clients). **Local precedence:** In hmlendea repositories, use NuciWeb.HTTP per csharp-nuget-usage guidance instead.
- Declare value-type properties of controller input models nullable, `required`, or `[JsonRequired]` so absent values are detected rather than defaulted (under-posting).
- Annotate every API controller action with an HTTP verb attribute (`[HttpGet]`, `[HttpPost]`, `[HttpPut]`, `[HttpPatch]`, `[HttpDelete]`).
- Check `ModelState.IsValid` in actions accepting model input, unless the controller has `[ApiController]` or an action filter performs validation.
- Annotate actions returning `IActionResult` or `ActionResult` with `[ProducesResponseType(typeof(T), StatusCodes.Status200OK)]` (or `[ProducesResponseType<T>]`) for each returned value type, or return `ActionResult<T>`. **Local precedence:** The controller instructions require non-generic `ActionResult`; use the attribute form.
