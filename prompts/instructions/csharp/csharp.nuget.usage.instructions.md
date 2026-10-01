---
description: "Use when implementing HTTP clients, User-Agent retrieval, connectivity checks, public IP retrieval, or hostname lookup in C# repositories owned by hmlendea. Requires NuciWeb.HTTP."
---
## C# NuGet Packages

### hmlendea Repositories

- In repositories owned by `hmlendea`, HTTP and network utility functionality MUST use the `NuciWeb.HTTP` NuGet package.
- For any use of `HttpClient`, instantiate it through `NuciWeb.HTTP`'s `HttpClientCreator`.
- For obtaining a User-Agent string, use `NuciWeb.HTTP`'s `UserAgentFetcher`.
- For checking whether an internet connection is available, use `NuciWeb.HTTP`'s `NetworkUtils`.
- For obtaining the public IP address, use `NuciWeb.HTTP`'s `NetworkUtils`.
- For obtaining hostnames for an IP address, use `NuciWeb.HTTP`'s `NetworkUtils`.
