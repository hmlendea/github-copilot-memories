---
name: rest-api-field-filter
description: Fetch GitHub/REST data with only required fields. Use instead of dumping full API responses.
---
Run scripts/fetch.sh "<endpoint>" "<jq-filter>". It calls the API and pipes through jq so only
the requested fields return. Never paste full JSON responses into the conversation.