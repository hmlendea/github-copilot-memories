# Python Rules: Platform APIs

One directive per Python rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Place `@receiver` above every other decorator on Django signal handlers.
- Set `safe=False` on Django `JsonResponse` when serialising non-dictionary objects.
- Never set `null=True` on Django string-based fields (`CharField` or `TextField`), except where `unique=True` and `blank=True` are both set.
- Never pass `locals()` to Django `render()`.
- Define Django `ModelForm` `Meta.fields` explicitly; never use `exclude` or `'__all__'`.
- Initialise reusable resources (clients and connections) at module level in AWS Lambda functions rather than within the handler; sensitive data is exempt.
- Never invoke other AWS Lambda functions synchronously from a Lambda function.
- Never hardcode the AWS region; read the `AWS_REGION` environment variable.
- Never start CloudWatch metric namespaces with `AWS/`.
- Return only JSON-serialisable values from AWS Lambda handlers.
- Never declare AWS Lambda handlers `async`.
- Never reassign reserved AWS Lambda environment variables (for example `AWS_REGION` or `_HANDLER`); use custom names.
- Set explicit timeouts on network calls in AWS Lambda functions.
- Catch and manage `botocore.exceptions.ClientError` explicitly.
- Delete temporary files in `/tmp` from AWS Lambda handlers (for example via `tempfile.NamedTemporaryFile`); files cached intentionally for later invocations are exempt.
- Use boto3 waiters instead of custom polling loops.
- Use boto3 paginators (`get_paginator`) or manual pagination for operations supporting pagination.
