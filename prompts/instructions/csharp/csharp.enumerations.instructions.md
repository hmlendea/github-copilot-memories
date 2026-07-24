---
description: "Use when writing or editing C# code. Covers namespaces, enumerations and enumeration classes."
applyTo: "**/*.{cs}"
---
## C#

### Namespaces

- Never create a `[xyz].Enumerations` (or `Enums`) namespace. Place enums in the same namespace and folder as the domain models they belong to.

### Enumerations & Enumeration Classes

- Use a regular `enum` for simple categorical values that carry no additional data and require no string serialisation.
- Use an **enumeration class** instead of an `enum` when any of the following apply:
  - Each value must carry additional structured data (e.g. multiple properties per value).
  - The value must serialise to and deserialise from a string reliably (e.g. stored in a database, returned in an API response).
  - The type needs custom equality semantics or operator overloads.

An enumeration class follows this exact structure:

```csharp
public class CheckInEligibility : IEquatable<CheckInEligibility>
{
    private static readonly Dictionary<string, CheckInEligibility> values = new()
    {
        { nameof(Allowed), new CheckInEligibility(nameof(Allowed)) },
        { nameof(Disallowed), new CheckInEligibility(nameof(Disallowed)) },
    };

    public string Name { get; }

    private CheckInEligibility(string name)
    {
        Name = name;
    }

    public static CheckInEligibility Allowed => values[nameof(Allowed)];
    public static CheckInEligibility Disallowed => values[nameof(Disallowed)];

    public static Array GetValues() => values.Values.ToArray();

    public static CheckInEligibility FromString(string name)
    {
        if (!values.ContainsKey(name))
        {
            return Disallowed;
        }

        return values[name];
    }

    public bool Equals(CheckInEligibility other)
    {
        if (other is null)
        {
            return false;
        }

        if (ReferenceEquals(this, other))
        {
            return true;
        }

        return Name == other.Name;
    }

    public override bool Equals(object obj)
    {
        if (obj is null)
        {
            return false;
        }

        if (ReferenceEquals(this, obj))
        {
            return true;
        }

        if (obj.GetType() != GetType())
        {
            return false;
        }

        return Equals((CheckInEligibility)obj);
    }

    public override int GetHashCode() => $"{nameof(CheckInEligibility)}:{Name}".GetHashCode();

    public override string ToString() => Name;

    public static bool operator ==(CheckInEligibility current, CheckInEligibility other) => current.Equals(other);

    public static bool operator !=(CheckInEligibility current, CheckInEligibility other) => !current.Equals(other);

    public static implicit operator string(CheckInEligibility eligibility) => eligibility.Name;
}
```

Rules for enumeration classes:

- The class must be `public` (not `sealed`; enumeration classes may be extended in some patterns, but if no extension is intended, `sealed` is acceptable).
- The backing dictionary must be `private static readonly` and use `nameof(...)` for both the key and the constructor argument, never string literals.
- Each value's static property uses `=>` (expression-bodied, not `{ get; }`).
- The constructor must be `private`.
- Always implement `IEquatable<T>`, override `Equals(object)` and `GetHashCode()`, and provide `==` / `!=` operator overloads.
- Always provide a `FromString(string name)` factory method. When the name is unrecognised, return a safe default (e.g. `Disallowed`) rather than throwing.
- Always provide `GetValues()` returning all registered values.
- Always provide an `implicit operator string` conversion so the value can be used directly where a string is expected.
- Place the enumeration class in the same namespace and folder as the domain model it belongs to, following the same rule as for regular enums.
