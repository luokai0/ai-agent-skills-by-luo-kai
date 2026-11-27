# Structured Data — ASI:One

Force ASI:One model responses to conform to a JSON schema using the `response_format` parameter. Essential for reliable data extraction and programmatic parsing.

---

## Quick Start (OpenAI SDK)

### TypeScript
```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.ASI_ONE_API_KEY!,
  baseURL: 'https://api.asi1.ai/v1',
});

const response = await client.chat.completions.create({
  model: 'asi1',
  messages: [
    { role: 'system', content: 'Extract the requested information as JSON.' },
    { role: 'user', content: 'Extract: John Smith is a 32 year old software engineer from San Francisco.' },
  ],
  response_format: {
    type: 'json_schema',
    json_schema: {
      name: 'person_info',
      strict: true,
      schema: {
        type: 'object',
        properties: {
          name: { type: 'string' },
          age: { type: 'integer' },
          occupation: { type: 'string' },
          city: { type: 'string' },
        },
        required: ['name', 'age', 'occupation', 'city'],
        additionalProperties: false,
      },
    },
  },
});

const result = JSON.parse(response.choices[0].message.content!);
console.log(result.name, result.age, result.occupation);
```

### Python
```python
import json
from openai import OpenAI

client = OpenAI(api_key="YOUR_ASI_ONE_API_KEY", base_url="https://api.asi1.ai/v1")

response = client.chat.completions.create(
    model="asi1",
    messages=[
        {"role": "system", "content": "Extract the requested information as JSON."},
        {"role": "user", "content": "Extract: John Smith is a 32-year-old software engineer from San Francisco."}
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person_info",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "occupation": {"type": "string"},
                    "city": {"type": "string"}
                },
                "required": ["name", "age", "occupation", "city"],
                "additionalProperties": False
            }
        }
    }
)

result = json.loads(response.choices[0].message.content)
print(f"Name: {result['name']}, Age: {result['age']}")
```

---

## Complex / Nested Schema

```typescript
const responseFormat = {
  type: 'json_schema' as const,
  json_schema: {
    name: 'order_summary',
    strict: true,
    schema: {
      type: 'object',
      additionalProperties: false,
      properties: {
        order_id: { type: 'string' },
        customer: {
          type: 'object',
          additionalProperties: false,
          properties: {
            name: { type: 'string' },
            email: { type: 'string' },
          },
          required: ['name', 'email'],
        },
        items: {
          type: 'array',
          items: {
            type: 'object',
            additionalProperties: false,
            properties: {
              sku: { type: 'string' },
              name: { type: 'string' },
              quantity: { type: 'integer' },
              unit_price: { type: 'number' },
            },
            required: ['sku', 'name', 'quantity', 'unit_price'],
          },
        },
        total: { type: 'number' },
        currency: { type: 'string' },
      },
      required: ['order_id', 'customer', 'items', 'total', 'currency'],
    },
  },
};

const response = await client.chat.completions.create({
  model: 'asi1',
  messages: [
    { role: 'system', content: 'Generate order data matching the schema.' },
    { role: 'user', content: 'Create a sample order for Jane Doe (jane@example.com) with 2 items totaling $150.' },
  ],
  response_format: responseFormat,
});

const order = JSON.parse(response.choices[0].message.content!);
```

---

## LangChain + Pydantic (Python)

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List

class Product(BaseModel):
    name: str = Field(description="Product name")
    price: float = Field(description="Price in USD")
    category: str = Field(description="Product category")

class ProductList(BaseModel):
    products: List[Product] = Field(description="List of extracted products")

llm = ChatOpenAI(
    model="asi1",
    base_url="https://api.asi1.ai/v1",
    api_key=os.getenv("ASI_ONE_API_KEY"),
)

structured_llm = llm.with_structured_output(ProductList)

text = """
Our store has:
- Wireless Mouse ($29.99) - Electronics
- Organic Coffee Beans ($14.50) - Groceries
- Running Shoes ($89.00) - Sports
"""

result = structured_llm.invoke(f"Extract all products:\n{text}")
for p in result.products:
    print(f"- {p.name}: ${p.price} ({p.category})")
```

---

## LangChain + Structured Output (TypeScript)

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { z } from 'zod';

const llm = new ChatOpenAI({
  model: 'asi1',
  openAIApiKey: process.env.ASI_ONE_API_KEY,
  configuration: { baseURL: 'https://api.asi1.ai/v1' },
});

const schema = z.object({
  title: z.string().describe('Movie title'),
  year: z.number().describe('Release year'),
  genre: z.string().describe('Primary genre'),
  reason: z.string().describe('Why this is recommended'),
});

const structuredLlm = llm.withStructuredOutput(schema);
const result = await structuredLlm.invoke('Recommend a sci-fi movie for someone who loved Inception');
console.log(result.title, result.year);
```

---

## Validation Pattern (TypeScript)

```typescript
import { z } from 'zod';

const PersonSchema = z.object({
  name: z.string(),
  age: z.number().int().positive(),
  city: z.string(),
});

type Person = z.infer<typeof PersonSchema>;

async function extractPerson(text: string): Promise<Person> {
  const response = await client.chat.completions.create({
    model: 'asi1',
    messages: [
      { role: 'system', content: 'Extract person info as JSON.' },
      { role: 'user', content: text },
    ],
    response_format: {
      type: 'json_schema',
      json_schema: {
        name: 'person',
        strict: true,
        schema: {
          type: 'object',
          properties: {
            name: { type: 'string' },
            age: { type: 'integer' },
            city: { type: 'string' },
          },
          required: ['name', 'age', 'city'],
          additionalProperties: false,
        },
      },
    },
  });

  const raw = JSON.parse(response.choices[0].message.content!);
  return PersonSchema.parse(raw); // Throws if invalid
}
```

---

## Best Practices

| Rule | Why |
|---|---|
| Always use `strict: true` | Guarantees schema adherence |
| Always set `additionalProperties: false` | Prevents extra fields |
| All properties in `required` array | Guarantees complete responses |
| Add `description` to each property | Helps model understand field purpose |
| Validate output (Zod/Pydantic) | Don't trust raw JSON in production |
| Use Pydantic/Zod over raw JSON | Cleaner, safer, type-safe |
| Add schema description comments | Improves extraction accuracy for complex schemas |
| Use system prompt | "Return ONLY valid JSON matching the provided schema" adds reliability |

---

## Raw Requests (No SDK)

```typescript
const response = await fetch('https://api.asi1.ai/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.ASI_ONE_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'asi1',
    messages: [
      { role: 'system', content: 'Return ONLY valid JSON matching the schema.' },
      { role: 'user', content: 'Generate a sample product...' },
    ],
    response_format: {
      type: 'json_schema',
      json_schema: {
        name: 'product',
        strict: true,
        schema: {
          type: 'object',
          properties: {
            name: { type: 'string' },
            price: { type: 'number' },
          },
          required: ['name', 'price'],
          additionalProperties: false,
        },
      },
    },
  }),
});

const data = await response.json();
const parsed = JSON.parse(data.choices[0].message.content);
```
