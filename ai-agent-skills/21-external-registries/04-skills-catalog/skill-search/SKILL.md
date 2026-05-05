---
name: skill-search
description: Search the Agent Skills Catalog to find skills by keyword, vendor, or category.
version: 1.0.0
license: MIT
author: "@anthropic-agent-skills"
tags:
  - search
  - catalog
  - discovery
---

## Instructions

Use this skill to search the skillscatalog.ai catalog for skills.

### Prerequisites

**Skill Key** - Get your key at https://skillscatalog.ai/settings/skill-keys

### How to Use

Search for skills:

```
Search the catalog for PDF tools
```

Get skill details:

```
python3 search_catalog.py --get anthropic/document-skills
```

List skills by vendor:

```
python3 search_catalog.py --vendor anthropic
```

### Output

```
Found 5 skills matching "pdf tools":

1. anthropic/document-skills
   Create and manipulate PDF documents
   Grade: A | Vendor: Anthropic

2. jeffrschneider/pdf-tools
   PDF conversion and extraction
   Grade: B | Vendor: jeffrschneider

3. acme/office-suite
   Office document processing including PDF
   Grade: A | Vendor: Acme Corp
```

### JSON Output

```bash
python3 search_catalog.py "pdf tools" --json
```

Returns:
```json
{
  "query": "pdf tools",
  "count": 5,
  "results": [
    {
      "vendorKey": "anthropic",
      "skillKey": "document-skills",
      "skillName": "Document Skills",
      "description": "Create and manipulate PDF documents",
      "rank": 0.95
    }
  ]
}
```

## Examples

**Basic search:**
```
User: Find skills for creating spreadsheets
Agent: Searching catalog for "spreadsheets"...

       Found 3 skills:
       1. anthropic/document-skills - Excel and spreadsheet creation
       2. datatools/xlsx-generator - Generate XLSX files
       3. office/sheets - Google Sheets integration
```

**Get skill details:**
```
User: Get details for anthropic/document-skills
Agent: Fetching skill details...

       anthropic/document-skills
       Description: Create and manipulate PDF documents
       Version: 1.2.0
       Safety Grade: A
       Vendor: Anthropic
```

## Limitations

- Requires internet connection
- Search results limited to public catalog
- Private org catalogs require org membership

## Dependencies

- Python 3.9+
- requests library
