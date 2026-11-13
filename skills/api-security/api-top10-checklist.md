# OWASP API Security Top 10:2023 — Detailed Checklist

Detailed checklist items for the OWASP API Security Top 10:2023, each with vulnerable patterns, remediation guidance, and a review checklist. See [SKILL.md](SKILL.md) for the procedure, findings classification, and report format, and `csharp-dotnet.md` for the C# and .NET supplement.

---

## API1:2023 — Broken Object Level Authorisation (BOLA)

**CWE:** CWE-285 (Improper Authorisation), CWE-639 (Authorisation Bypass Through User-Controlled Key)
**Severity:** Critical to High

BOLA arises where an API endpoint accepts an object identifier from the client and does not verify that the authenticated user is authorised to reach that specific object. It is the most prevalent and most critical API weakness.

### What to Examine

- Endpoints accepting resource identifiers in the path, query parameters, or request body.
- Authorisation logic verifying only that the user is authenticated, not that the user possesses or may reach the object.
- Sequential or predictable identifiers (auto-increment integers) permitting enumeration.
- Batch and list endpoints returning objects without filtering by the caller's permissions.
- Authorisation enforced solely at the route tier, leaving data-access paths reachable from elsewhere.

### REST Vulnerable Patterns

```python
# VULNERABLE: No ownership check -- any authenticated user can access any order
@app.route('/api/v1/orders/<order_id>', methods=['GET'])
@require_auth
def get_order(order_id):
    order = db.orders.find_one({"_id": order_id})
    return jsonify(order)
```

Remediation:

```python
# SECURE: Verify the authenticated user owns the requested resource
@app.route('/api/v1/orders/<order_id>', methods=['GET'])
@require_auth
def get_order(order_id):
    order = db.orders.find_one({"_id": order_id, "user_id": current_user.id})
    if not order:
        return jsonify({"error": "Not found"}), 404
    return jsonify(order)
```

### GraphQL Vulnerable Patterns

```graphql
# VULNERABLE: Any authenticated user can query any user's private data
type Query {
  user(id: ID!): User
  order(id: ID!): Order
}
```

```javascript
// VULNERABLE: Resolver fetches object without ownership validation
const resolvers = {
  Query: {
    order: async (_, { id }, context) => {
      return await Order.findById(id);  // No authorisation check
    },
  },
};
```

Remediation:

```javascript
// SECURE: Resolver enforces ownership before returning data
const resolvers = {
  Query: {
    order: async (_, { id }, context) => {
      const order = await Order.findById(id);
      if (!order || order.userId !== context.user.id) {
        throw new ForbiddenError("Not authorised");
      }
      return order;
    },
  },
};
```

### BOLA versus BFLA

BOLA and BFLA (API5:2023) are frequently confused. The distinction matters for accurate findings.

| Aspect | BOLA (API1) | BFLA (API5) |
|---|---|---|
| **What is bypassed** | Object-level access (horizontal) | Function-level access (vertical) |
| **Attack vector** | Manipulate a resource identifier to reach another user's object | Invoke an operation intended for a different role or privilege level |
| **Example** | Regular user reaches `GET /api/orders/9999` belonging to another user | Regular user invokes `DELETE /api/admin/users/42` intended for administrators |
| **Authorisation gap** | Absent ownership or relationship check upon the data object | Absent role or permission check upon the operation |
| **CWE** | CWE-639 (User-Controlled Key) | CWE-285 (Improper Authorisation) |

Both can coexist within one endpoint. An endpoint may lack both a role check (BFLA) and an ownership check (BOLA).

### Review Checklist

- [ ] Every endpoint accepting a resource identifier enforces ownership or relationship-based access control.
- [ ] Authorisation checks occur at the data-access tier, not solely at the controller or route tier.
- [ ] Batch and list endpoints filter results by the caller's permissions.
- [ ] Resource identifiers are UUIDs or non-sequential values, resisting enumeration.
- [ ] GraphQL resolvers enforce authorisation upon every field returning sensitive data.

---

## API2:2023 — Broken Authentication

**CWE:** CWE-287 (Improper Authentication), CWE-307 (Improper Restriction of Excessive Authentication Attempts), CWE-798 (Use of Hard-coded Credentials)
**Severity:** Critical to High

APIs are particularly susceptible to authentication weaknesses because they expose machine-consumable endpoints lacking the browser-based protections (cookies, CSRF tokens, CAPTCHA) customary in traditional web applications.

### What to Examine

- Authentication endpoints without brute-force protection (rate limiting, account lockout, CAPTCHA).
- JWT validation that is absent or incomplete — no signature verification, no expiration check, acceptance of the `none` algorithm, algorithm confusion.
- API keys transmitted in URL query strings (recorded in access logs, browser history, and proxies).
- Absent or weak token rotation — refresh tokens that never expire or are not rotated upon use.
- Password reset and account recovery processes leaking tokens or permitting enumeration.
- Service-to-service communication without authentication (implicit trust based upon network location).

### Vulnerable Patterns

```python
# VULNERABLE: JWT signature not verified
import jwt
token_data = jwt.decode(token, options={"verify_signature": False})
```

```javascript
// VULNERABLE: No rate limiting on authentication endpoint
app.post('/api/v1/auth/login', async (req, res) => {
  const user = await User.findOne({ email: req.body.email });
  if (user && await bcrypt.compare(req.body.password, user.password)) {
    return res.json({ token: generateJWT(user) });
  }
  return res.status(401).json({ error: "Invalid credentials" });
});
```

```yaml
# VULNERABLE: API key in query parameter (recorded in access logs)
paths:
  /api/v1/data:
    get:
      parameters:
        - name: api_key
          in: query  # Should be in header
```

### Remediation Guidance

- Enforce rate limiting upon all authentication endpoints (for example five attempts per minute per address or account).
- Validate JWT signatures using a strong algorithm (RS256, ES256). Reject `none`, and reject `HS256` where RSA is expected (algorithm confusion attack).
- Transmit API keys and tokens in HTTP headers (the `Authorization` header), never in URL query strings.
- Implement token expiration: access tokens (5–15 minutes), refresh tokens (hours to days, rotated upon use).
- Use `bcrypt`, `scrypt`, or `Argon2id` for password storage.
- Authenticate service-to-service calls with mTLS or signed tokens, not network-based trust.

### Review Checklist

- [ ] All authentication endpoints possess brute-force protections (rate limiting, lockout).
- [ ] JWTs are validated for signature, expiration (`exp`), issuer (`iss`), and audience (`aud`).
- [ ] The `none` algorithm and algorithm confusion attacks are prevented by an explicit algorithm allowlist.
- [ ] API keys and tokens are transmitted in headers, not query strings.
- [ ] Refresh tokens are rotated upon each use and are revocable.
- [ ] Service-to-service communication is explicitly authenticated.

---

## API3:2023 — Broken Object Property Level Authorisation

**CWE:** CWE-213 (Exposure of Sensitive Information Due to Incompatible Policies), CWE-915 (Improperly Controlled Modification of Dynamically-Determined Object Attributes)
**Severity:** High to Medium

This risk covers two related problems: excessive data exposure (the API returns more object properties than the client requires, including sensitive fields) and mass assignment (the API accepts and processes more properties than it should, permitting clients to modify fields outside their authority).

### Vulnerable Patterns

```python
# VULNERABLE: Excessive data exposure -- returns all fields including sensitive ones
@app.route('/api/v1/users/<user_id>')
@require_auth
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.to_dict())  # Includes password_hash, ssn, internal_role
```

```python
# VULNERABLE: Mass assignment -- client can set any field including role
@app.route('/api/v1/users/profile', methods=['PUT'])
@require_auth
def update_profile():
    current_user.update(**request.json)  # Client can send {"role": "admin"}
    db.session.commit()
    return jsonify(current_user.to_dict())
```

```javascript
// VULNERABLE: GraphQL exposes sensitive fields with no restriction
const UserType = new GraphQLObjectType({
  name: 'User',
  fields: {
    id: { type: GraphQLID },
    email: { type: GraphQLString },
    passwordHash: { type: GraphQLString },  // Should never be exposed
    role: { type: GraphQLString },
    ssn: { type: GraphQLString },            // Requires field-level auth
  },
});
```

### Remediation Guidance

- Define explicit response schemas (DTOs or serialisers) for every endpoint. Never return unprocessed database objects.
- Use allowlists for writable fields upon update and create operations. Never bind request bodies directly to models.
- In GraphQL, implement field-level authorisation directives or resolver-level checks for sensitive fields.
- Strip sensitive properties (`password_hash`, `internal_id`, `role`, `ssn`) from all responses unless the endpoint expressly requires them for an authorised consumer.

### Review Checklist

- [ ] Every API response uses a defined schema or serialiser enumerating the returned fields.
- [ ] Sensitive fields (credentials, personal data, internal metadata) are excluded from standard responses.
- [ ] Update endpoints use an allowlist of modifiable fields; mass assignment is impossible.
- [ ] GraphQL fields carrying sensitive data possess resolver-level authorisation.
- [ ] The API specification accurately reflects the genuine response schema.

---

## API4:2023 — Unrestricted Resource Consumption

**CWE:** CWE-770 (Allocation of Resources Without Limits or Throttling), CWE-400 (Uncontrolled Resource Consumption), CWE-799 (Improper Control of Interaction Frequency)
**Severity:** High to Medium

### Vulnerable Patterns

```python
# VULNERABLE: No pagination limit -- client can request all records
@app.route('/api/v1/transactions')
@require_auth
def list_transactions():
    limit = request.args.get('limit', type=int)  # No max; client sends limit=1000000
    transactions = Transaction.query.filter_by(user_id=current_user.id).limit(limit).all()
    return jsonify([t.to_dict() for t in transactions])
```

```graphql
# VULNERABLE: GraphQL allows deeply nested queries (denial of service)
query {
  users {
    friends {
      friends {
        friends {
          friends {
            name
          }
        }
      }
    }
  }
}
```

```javascript
// VULNERABLE: No request body size limit
app.use(express.json()); // Default limit may be very large or unconfigured
```

### Remediation Guidance

- Implement rate limiting at the gateway and application tiers. Use sliding-window or token-bucket algorithms. Set per-endpoint limits on the basis of expected legitimate usage.
- Enforce a maximum pagination size (for example `limit` capped at 100). Default to a reasonable page size (for example 20).
- Set maximum request body sizes (`express.json({ limit: '1mb' })`).
- For GraphQL: enforce query depth limits (for example maximum depth 5), complexity analysis (weighted field costs), and batch query limits.
- Set execution timeouts for database queries and downstream API calls.
- Implement cost alerts and circuit breakers for operations triggering billable third-party APIs.

### Review Checklist

- [ ] Rate limiting is configured for all endpoints, with stricter limits upon expensive operations.
- [ ] Pagination enforces a maximum page size server-side.
- [ ] Request body size limits are configured.
- [ ] GraphQL queries possess depth limits, complexity limits, and batch restrictions.
- [ ] Database queries and downstream calls possess execution timeouts.
- [ ] Billable operations possess cost controls and alerting.

---

## API5:2023 — Broken Function Level Authorisation (BFLA)

**CWE:** CWE-285 (Improper Authorisation)
**Severity:** Critical to High

### Vulnerable Patterns

```python
# VULNERABLE: No role check -- any authenticated user can delete any user
@app.route('/api/v1/admin/users/<user_id>', methods=['DELETE'])
@require_auth  # Checks authentication but not authorisation
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return jsonify({"status": "deleted"})
```

```javascript
// VULNERABLE: GraphQL mutation lacks role enforcement
const resolvers = {
  Mutation: {
    setUserRole: async (_, { userId, role }, context) => {
      // Any authenticated user can set roles -- no admin check
      return await User.findByIdAndUpdate(userId, { role });
    },
  },
};
```

### Remediation Guidance

- Implement centralised authorisation middleware or a policy engine enforcing role and permission checks consistently throughout all endpoints.
- Deny by default: every endpoint should require an explicit permission grant. Do not rely upon the obscurity of administrative URL paths.
- Enforce authorisation upon every HTTP method independently. A user authorised to `GET` a resource is not thereby authorised to `DELETE` it.
- In GraphQL, use directive-based or middleware-based authorisation upon mutations (`@hasRole(role: ADMIN)`).
- Audit the endpoint inventory against the authorisation policy matrix regularly, detecting gaps.

### Review Checklist

- [ ] All administrative and privileged endpoints enforce role-based authorisation.
- [ ] Authorisation middleware is centralised and applied consistently.
- [ ] Each HTTP method upon each endpoint possesses an independent authorisation check.
- [ ] GraphQL mutations enforce role or permission checks within resolvers or directives.
- [ ] The authorisation policy is deny-by-default; endpoints are inaccessible unless expressly permitted.

---

## API6:2023 — Unrestricted Access to Sensitive Business Processes

**CWE:** CWE-799 (Improper Control of Interaction Frequency), CWE-837 (Improper Enforcement of a Single, Unique Action)
**Severity:** High to Medium

### Vulnerable Patterns

```python
# VULNERABLE: No anti-automation on purchase process
@app.route('/api/v1/tickets/purchase', methods=['POST'])
@require_auth
def purchase_ticket():
    ticket = find_available_ticket(request.json['event_id'])
    if ticket:
        ticket.assign_to(current_user)
        charge_payment(current_user, ticket.price)
        return jsonify({"ticket_id": ticket.id}), 200
    return jsonify({"error": "Sold out"}), 409
```

### Remediation Guidance

- Implement business-level rate limiting based upon user identity, not merely address (for example maximum four ticket purchases per user per event).
- Add CAPTCHA or proof-of-work challenges upon business-critical processes that should be human-initiated.
- Use device fingerprinting and behavioural analysis to detect automated access patterns.
- Implement velocity checks: flag or block accounts performing business operations at inhuman velocity.
- Consider step-up verification (short message service or electronic mail confirmation) for high-value operations.

### Review Checklist

- [ ] Business-critical processes possess per-user velocity limits appropriate to the business context.
- [ ] Anti-automation controls (CAPTCHA, proof-of-work) are in place upon human-initiated processes.
- [ ] Device fingerprinting or behavioural analysis distinguishes human from automated traffic.
- [ ] High-value operations require step-up verification.
- [ ] Business-logic abuse scenarios are documented and monitored.

---

## API7:2023 — Server Side Request Forgery (SSRF)

**CWE:** CWE-918 (Server-Side Request Forgery)
**Severity:** High

### Vulnerable Patterns

```python
# VULNERABLE: Fetches any URL provided by the user
@app.route('/api/v1/preview', methods=['POST'])
@require_auth
def url_preview():
    url = request.json['url']
    response = requests.get(url)  # Attacker sends http://169.254.169.254/latest/meta-data/
    return jsonify({"content": response.text[:500]})
```

```python
# VULNERABLE: Webhook registration accepts any URL
@app.route('/api/v1/webhooks', methods=['POST'])
@require_auth
def register_webhook():
    webhook_url = request.json['url']  # Attacker registers http://internal-service:8080/admin
    Webhook.create(user_id=current_user.id, url=webhook_url)
    return jsonify({"status": "registered"})
```

### Remediation Guidance

- Validate and sanitise all user-supplied destinations. Use an allowlist of permitted schemes (`https` only), domains, or address ranges.
- Resolve hostnames and reject private and reserved ranges: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`, `169.254.0.0/16` (cloud metadata), `fd00::/8` (IPv6 unique local addresses).
- Deactivate HTTP redirects, or revalidate the destination following a redirect.
- Use a dedicated egress proxy for outbound requests, enforcing domain allowlists.
- In cloud environments, use IMDSv2 (token-based metadata access) to mitigate SSRF exploitation against cloud metadata services.
- Do not return raw responses from retrieved destinations to the client; extract only the required data.

### Review Checklist

- [ ] All user-supplied destinations are validated against a scheme and domain allowlist.
- [ ] Resolved addresses are checked against private and internal ranges before the request is made.
- [ ] HTTP redirects are deactivated, or the final destination is revalidated.
- [ ] Cloud metadata endpoint access is restricted (IMDSv2 upon AWS, equivalents upon GCP and Azure).
- [ ] Raw responses from retrieved destinations are never returned directly to the client.

---

## API8:2023 — Security Misconfiguration

**CWE:** CWE-16 (Configuration), CWE-611 (Improper Restriction of XML External Entity Reference), CWE-942 (Permissive Cross-domain Policy with Untrusted Domains)
**Severity:** High to Medium

### Vulnerable Patterns

```python
# VULNERABLE: Overly permissive CORS
from flask_cors import CORS
CORS(app, origins="*", supports_credentials=True)  # Allows any origin with credentials
```

```javascript
// VULNERABLE: Verbose error messages in production
app.use((err, req, res, next) => {
  res.status(500).json({
    error: err.message,
    stack: err.stack,       // Exposes internal details
    query: err.sql,         // Exposes database queries
  });
});
```

```java
// VULNERABLE: XXE enabled in XML parser
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
// No XXE protections configured
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(request.getInputStream());
```

### Remediation Guidance

- Configure CORS with an explicit allowlist of permitted origins. Never use `*` together with `credentials: true`.
- Set security response headers upon all API responses:
  - `Strict-Transport-Security: max-age=31536000; includeSubDomains`
  - `X-Content-Type-Options: nosniff`
  - `Cache-Control: no-store` upon sensitive responses
- Return generic error messages in production. Record detailed errors server-side with correlation identifiers.
- Deactivate unnecessary HTTP methods. Return `405 Method Not Allowed` for unsupported methods.
- Deactivate XML external entity processing: set `factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`.
- Enforce TLS 1.2 or later with strong cipher suites. Deactivate TLS 1.0 and 1.1.
- Automate configuration scanning in CI/CD to detect drift from security baselines.

### Review Checklist

- [ ] CORS is configured with an explicit origin allowlist; the wildcard is not combined with credentials.
- [ ] Security headers are present upon all API responses.
- [ ] Error responses in production are generic; no stack traces, SQL queries, or internal paths.
- [ ] Only required HTTP methods are enabled per endpoint.
- [ ] TLS 1.2 or later is enforced with strong cipher suites.
- [ ] XML parsers deactivate external entity processing and document type definition loading.
- [ ] Default credentials are changed or eliminated upon all infrastructure components.

---

## API9:2023 — Improper Inventory Management

**CWE:** CWE-1059 (Insufficient Technical Documentation)
**Severity:** Medium

### What to Examine

- Multiple API versions operating simultaneously (`/api/v1/`, `/api/v2/`, `/api/v3/`) where older versions lack security patches.
- Debug or test endpoints present in production (`/api/debug/`, `/api/test/`, `/api/internal/`, `/graphql/playground`).
- Undocumented endpoints present in code but absent from the specification.
- Endpoints exposed to the public internet that should remain internal.
- Deprecated endpoints remaining functional beyond the announced retirement date.
- Divergent security configuration between environments (staging permits unauthenticated access while production does not, yet staging is publicly reachable).

### Review Procedure

```text
1. Extract all route definitions from source code (Grep for route decorators, handler registrations).
2. Compare against the published OpenAPI/Swagger specification.
3. Flag any endpoint present in code but missing from documentation (shadow API).
4. Flag any endpoint marked as deprecated that is still reachable.
5. Check for environment-specific routes (debug, test, internal) that should not exist in production.
6. Verify that older API versions have equivalent security controls to current versions.
```

### Remediation Guidance

- Maintain one authoritative API inventory. Generate specifications from code, or validate code against specifications in CI/CD.
- Retire deprecated API versions upon a defined schedule. Redirect older versions to the current version, or return `410 Gone`.
- Remove debug, test, and playground endpoints from production builds using build-time flags or environment checks.
- Segment internal APIs from external APIs at the network tier (separate gateways, virtual network isolation).
- Scan for shadow APIs by comparing routing tables against documentation upon every deployment.

### Review Checklist

- [ ] The API inventory is documented and matches the genuinely deployed endpoints.
- [ ] Deprecated API versions are retired or possess equivalent security controls.
- [ ] No debug, test, or playground endpoints are reachable in production.
- [ ] Internal APIs are not reachable from external networks.
- [ ] CI/CD pipelines validate that code routes match the API specification.

---

## API10:2023 — Unsafe Consumption of APIs

**CWE:** CWE-20 (Improper Input Validation), CWE-295 (Improper Certificate Validation), CWE-319 (Cleartext Transmission of Sensitive Information)
**Severity:** High to Medium

### Vulnerable Patterns

```python
# VULNERABLE: Third-party API data used in SQL without sanitisation
partner_data = requests.get("https://partner-api.example.com/products").json()
for product in partner_data:
    db.execute(f"INSERT INTO products (name) VALUES ('{product['name']}')")
```

```python
# VULNERABLE: TLS certificate verification disabled
response = requests.get("https://third-party-api.com/data", verify=False)
```

```javascript
// VULNERABLE: Upstream API data rendered without escaping
const enrichmentData = await fetch('https://enrichment-api.com/user/' + userId);
const data = await enrichmentData.json();
res.send(`<div class="bio">${data.biography}</div>`);  // Stored XSS via third party
```

### Remediation Guidance

- Treat all data from external and internal APIs as untrusted input. Validate and sanitise before use.
- Always enforce TLS certificate validation upon outbound connections. Never set `verify=False` or `rejectUnauthorized: false` in production.
- Validate upstream response schemas using a schema validator (JSON Schema, Pydantic, Zod).
- Implement timeouts, retry limits with backoff, and circuit breakers upon all outbound API calls.
- Restrict redirects upon outbound calls. Where redirects are followed, revalidate the destination.
- Use parameterised queries when inserting data from any source, including trusted internal APIs.

### Review Checklist

- [ ] Data from all upstream APIs is validated and sanitised before use in queries, rendering, or commands.
- [ ] TLS certificate validation is enabled upon all outbound API calls.
- [ ] Response schemas from third-party APIs are validated before processing.
- [ ] Outbound calls possess timeouts, retry limits, and circuit breakers.
- [ ] Redirect following is deactivated or restricted upon outbound HTTP calls.
