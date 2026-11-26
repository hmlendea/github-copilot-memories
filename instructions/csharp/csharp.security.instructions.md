---
description: "Use for C# security, sensitive data, personal data, masking, logs, exception messages, telemetry, secrets, or configuration values."
---
## C#

### Security
- Never disclose sensitive data in logs, exception messages, or telemetry without masking it. This includes PAN/card numbers, CVV, passwords, keys, tokens, connection strings, and personal data, including names, e-mail addresses, phone numbers, postal addresses, IP addresses, and account identifiers.
- Never hardcode secrets, connection strings, or machine-specific paths in source code or tracked configuration files (`appsettings*.json`, `launchSettings.json`). Read them at runtime from user secrets, environment variables, or a secret store; retain placeholders only in tracked files.

### Security Rules

One directive per C# security rule. Thresholds reflect the strictest values.

#### Secrets, Credentials And Authentication
- Never hardcode IP addresses; read them from configuration. Exempt: loopback (`127.0.0.0/8`, `::1`), `0.0.0.0`, `255.255.255.255`, OID-like `2.5.x.x` values, and documentation address blocks.
- Never hardcode credentials in string literals, connection strings, or URLs (keywords: `password`, `passwd`, `pwd`, `passphrase`); read them from a secret store or configuration at run time.
- Never connect to a database without a password or with a zero-length password.
- Authenticate LDAP connections; never use `AuthenticationTypes.None` or anonymous binds.
- Never hardcode secrets (API keys, authentication tokens, credentials, other secrets, or random-looking strings in variables named for them) in source; read them from a secret store or configuration at run time.
- Never disclose JWT signing keys; read them from a secret store, and never hardcode or log them.

#### Injection And User-Controlled Input
- Never pass user-controlled data to OS command execution (`Process.Start`, `ProcessStartInfo.FileName`); use fixed commands.
- Never compose SQL queries via concatenation, interpolation, or `string.Format` with variable data; use parameterised commands (`SqlParameter`, Entity Framework `FromSql`/`FromSqlInterpolated`).
- Never compose LDAP queries from user-controlled data without escaping; encode filter values.
- Never construct regular expressions from user-controlled data; escape it with `Regex.Escape` and specify a timeout.
- Never construct SQL from user-controlled data; use parameterised queries.
- Never log user-controlled data without neutralising line breaks and control characters (CR/LF).
- Never construct NoSQL queries (for example MongoDB filters or JSON queries) from user-controlled strings; use typed filter builders.
- Never compile or execute code constructed from user-controlled data (`CSharpCodeProvider`, Roslyn scripting, dynamic LINQ).
- Never pass user-controlled data as OS command arguments without validation; use `ProcessStartInfo.ArgumentList` and decline option-like values (a leading `-`).
- Never load types or assemblies, or invoke members, by names taken from user-controlled data (`Type.GetType`, `Activator.CreateInstance`, `GetMethod`); map input to an enumerated permitted set.
- Never compose OS command arguments from user-controlled input; validate it against an enumerated set of permitted values.
- Specify a timeout for every `Regex` (constructor or static method), or use `RegexOptions.NonBacktracking`.
- Never set environment variables from user-controlled data.
- Never size memory allocations (arrays, buffers, `StringBuilder` capacity) from user-controlled values without a maximum bound.
- Never construct connection strings from user-controlled data; use a `DbConnectionStringBuilder` with validated values.
- Never use user-controlled values as loop bounds without a maximum.

#### Files, Archives And Processes
- Never construct file paths from user-controlled data without canonicalising them and verifying they remain within the intended base directory.
- Never grant file or directory permissions to everyone (for example `FileSystemRights` for `Everyone`, Unix mode `0777`); apply least privilege.
- Start OS processes via fully qualified executable paths, never via `PATH` lookup.
- When expanding archives, cap the total uncompressed size, the number of items, and the compression ratio to prevent zip bombs.
- Never store sensitive files in publicly writable directories (`/tmp`, `/var/tmp`, a manually composed `%TEMP%` location); use dedicated directories with restricted permissions.
- Never create temporary files with `Path.GetTempFileName()`; use `Path.GetRandomFileName()` with `FileMode.CreateNew` and restricted permissions.
- When extracting archives, resolve each item's destination and verify it remains within the extraction directory (zip slip).
- Never let user-controlled data select which files are accessed in a manner that reveals file existence (filesystem oracle); map input to an enumerated permitted set.

#### XML And Deserialisation
- Never construct XPath expressions from user-controlled data; use parameterised XPath (`XsltArgumentList` variables) or strict validation.
- Deactivate DTD processing and external entity resolution in XML parsers (`DtdProcessing.Prohibit`, `XmlResolver = null`).
- Never deserialise user-controlled data with insecure deserialisers (`BinaryFormatter`, `NetDataContractSerializer`, `SoapFormatter`, `LosFormatter`, `ObjectStateFormatter`, Json.NET `TypeNameHandling` other than `None`).
- Validate invariants in deserialisation constructors and `[OnDeserialized]` callbacks of `[Serializable]` types; deserialisation bypasses validating constructors.
- Restrict deserialised types to an enumerated permitted set (`SerializationBinder`, known types); never deserialise arbitrary types.
- Validate XML signatures with a pre-configured key (`CheckSignature(key)`), never only with key information embedded in the document.
- Never construct XML documents or nodes by concatenating user-controlled data; use XML APIs that encode values.
- Never load XSLT stylesheets from user-controlled sources; deactivate script and the `document()` function (`XsltSettings.Default`).

#### Cryptography And TLS
- Hash passwords with a cryptographically random salt of at least 16 bytes, unique per password.
- Never use `System.Random` for security-sensitive values (tokens, keys, passwords, nonces); use `RandomNumberGenerator`.
- Never implement custom cryptographic algorithms; use vetted platform implementations.
- Generate a cryptographically random IV for every CBC encryption; never reuse or hardcode IVs.
- Never initialise secure random generators (for example BouncyCastle `SecureRandom`) with predictable or constant values.
- Use TLS 1.2 or later; never activate SSL 3.0, TLS 1.0, or TLS 1.1 (`SslProtocols`, `ServicePointManager.SecurityProtocol`).
- Use RSA and DSA keys of at least 2048 bits and elliptic curves of at least 224 bits.
- Never use MD5, SHA-1, RIPEMD-160, or other weak hash functions for security purposes; use SHA-256 or above.
- Never deactivate server certificate validation (a `ServerCertificateCustomValidationCallback` returning `true`, `DangerousAcceptAnyServerCertificateValidator`).
- Store passwords only as salted slow hashes (PBKDF2 with at least 600,000 iterations for SHA-256, 210,000 for SHA-512, or 1,300,000 for SHA-1; or bcrypt, scrypt, or Argon2); never in plaintext or with rapid general-purpose hashes.
- Use authenticated encryption (for example AES-GCM) or CBC combined with an HMAC; never use ECB mode, and use OAEP padding for RSA, never PKCS#1 v1.5.
- Use robust ciphers (AES); never DES, 3DES, RC2, RC4, or Blowfish.
- Sign and verify JWTs with robust algorithms; never accept `none` or deactivate signature validation (`ValidateIssuerSigningKey`, `RequireSignedTokens`).

#### Web, Cookies And Transport
- Set `Secure = true` on every cookie (`CookieOptions`, `HttpCookie`).
- Set `HttpOnly = true` on every cookie unless client-side script explicitly requires access to it.
- Never deactivate CSRF protection (`[IgnoreAntiforgeryToken]`, omitted antiforgery validation); validate antiforgery tokens on state-changing endpoints that use cookie authentication.
- Never ship debugging capabilities to production; guard `UseDeveloperExceptionPage` and similar diagnostics with `env.IsDevelopment()`.
- Never permit all origins in CORS (`AllowAnyOrigin()`, `*`, reflected `Origin` headers); enumerate specific authorised origins.
- Encode user-controlled data for its HTML or JavaScript context in HTTP responses; never emit it unencoded (`Html.Raw`, `Response.Write`).
- Never issue server-side requests to URLs constructed from user-controlled data; validate scheme and host against an enumerated permitted set.
- Never redirect to user-controlled URLs; use `LocalRedirect`, `Url.IsLocalUrl`, or an enumerated permitted set.
- Use encrypted protocols (`https`, `ftps`, `sftp`, `ssh`, SMTP with TLS) instead of clear-text ones (`http`, `ftp`, `telnet`, unencrypted SMTP). Exempt: loopback addresses and `localhost`.
- Never deactivate request body limits (`[DisableRequestSizeLimit]`, `MaxRequestBodySize = null`) or set them (`[RequestSizeLimit]`, `[RequestFormLimits]`, Kestrel `MaxRequestBodySize`) above 8,000,000 bytes.
- Never deactivate ASP.NET request validation (`[ValidateInput(false)]`, a reduced `requestValidationMode`).
- Never create session cookies or session identifiers from user-controlled data; let the platform generate them.
- Never disclose stack traces or exception details to clients; return generic error responses and log the details on the server.
- Configure restrictive Content Security Policies; never permit `unsafe-inline`, `unsafe-eval`, or `*` sources.
- Never insert user-controlled data into server-side request URL paths without encoding and validating each segment (traversal via `..`).

#### Platform And Runtime
- Never call `CoSetProxyBlanket` or `CoInitializeSecurity`.
- Never declare member transparency annotations (`[SecurityCritical]`, `[SecuritySafeCritical]`) that conflict with the containing type's or assembly's annotation.
- Review logger configuration for security: never log sensitive data, restrict access to log destinations, and neutralise user-controlled values in logs.
- Never use `unsafe` code blocks unless strictly necessary; review each one for memory safety.
