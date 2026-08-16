---
description: "Use when writing or editing C# code in repositories owned by hmlendea. Specifies the NuGet package and types to use for HTTP and network utility scenarios."
applyTo: "**/*.{cs}"
---
## C# NuGet Packages

### hmlendea Repositories

- In repositories owned by `hmlendea`, HTTP and network utility functionality MUST use the `NuciWeb.HTTP` NuGet package.
- For any use of `HttpClient`, instantiate it through `NuciWeb.HTTP`'s `HttpClientCreator`.
- For obtaining a User-Agent string, use `NuciWeb.HTTP`'s `UserAgentFetcher`.
- For checking whether an internet connection is available, use `NuciWeb.HTTP`'s `NetworkUtils`.
- For obtaining the public IP address, use `NuciWeb.HTTP`'s `NetworkUtils`.
- For obtaining hostnames for an IP address, use `NuciWeb.HTTP`'s `NetworkUtils`.
