---
name: lap-ace-provisioning-managementpartner-api
description: "ACE Provisioning ManagementPartner API skill. Use when working with ACE Provisioning ManagementPartner for providers. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
metadata:
  openclaw:
    requires:
      env:
        - ACE_PROVISIONING_MANAGEMENTPARTNER_API_KEY
---

# ACE Provisioning ManagementPartner API
API version: 2018-02-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.ManagementPartner/operations -- verify access

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.ManagementPartner/partners/{partnerId} | Get a specific `Partner`. |
| PUT | /providers/Microsoft.ManagementPartner/partners/{partnerId} | Create a specific `Partner`. |
| PATCH | /providers/Microsoft.ManagementPartner/partners/{partnerId} | Update a specific `Partner`. |
| DELETE | /providers/Microsoft.ManagementPartner/partners/{partnerId} | Delete a specific `Partner`. |
| GET | /providers/Microsoft.ManagementPartner/operations | Get operations. |
| GET | /providers/Microsoft.ManagementPartner/partners | Get a specific `Partner`. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get partner details?" -> GET /providers/Microsoft.ManagementPartner/partners/{partnerId}
- "Update a partner?" -> PUT /providers/Microsoft.ManagementPartner/partners/{partnerId}
- "Partially update a partner?" -> PATCH /providers/Microsoft.ManagementPartner/partners/{partnerId}
- "Delete a partner?" -> DELETE /providers/Microsoft.ManagementPartner/partners/{partnerId}
- "List all operations?" -> GET /providers/Microsoft.ManagementPartner/operations
- "List all partners?" -> GET /providers/Microsoft.ManagementPartner/partners
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## CLI

```bash
# Update this spec to the latest version
npx @lap-platform/lapsh get ace-provisioning-managementpartner-api -o references/api-spec.lap

# Search for related APIs
npx @lap-platform/lapsh search ace-provisioning-managementpartner-api
```

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
