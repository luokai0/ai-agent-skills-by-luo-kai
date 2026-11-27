# OpenAI Compatibility & LangChain — ASI:One

ASI:One is **fully compatible** with OpenAI's Chat Completions API. Just swap `base_url` — everything else stays the same.

---

## SDK Setup

### TypeScript / Node.js
```bash
npm install openai
```

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.ASI_ONE_API_KEY!,
  baseURL: 'https://api.asi1.ai/v1',
});
```

### Python
```bash
pip install openai
```

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_ASI_ONE_API_KEY",
    base_url="https://api.asi1.ai/v1"
)
```

---

## Standard OpenAI Parameters (all work as-is)

| Parameter | Type | Notes |
|---|---|---|
| `model` | string | Use ASI:One model names (`asi1`, `asi1-mini`, etc.) |
| `messages` | array | Standard chat array |
| `temperature` | float | 0–2 |
| `max_tokens` | integer | Max response tokens |
| `top_p` | float | Nucleus sampling |
| `frequency_penalty` | float | -2.0 to 2.0 |
| `presence_penalty` | float | -2.0 to 2.0 |
| `stream` | boolean | SSE streaming |
| `tools` | array | Function calling |
| `tool_choice` | string/object | Tool selection control |
| `response_format` | object | JSON schema output |

## ASI:One-Specific Parameters

| Parameter | Location | Notes |
|---|---|---|
| `web_search` | body (`extra_body`) | Enable built-in web search |
| `x-session-id` | header (`extra_headers`) | Session persistence for agentic models |
| `agent_address` | body | Target specific Agentverse agent |
| `planner_mode` | body | Enable ASI Planner |
| `study_mode` | body | Enable study/research mode |

---

## Full Examples

### Basic Completion (TypeScript)
```typescript
const response = await client.chat.completions.create({
  model: 'asi1',
  messages: [
    { role: 'system', content: 'Be precise and concise.' },
    { role: 'user', content: 'What is agentic AI?' },
  ],
  temperature: 0.2,
  top_p: 0.9,
  max_tokens: 1000,
  presence_penalty: 0,
  frequency_penalty: 0,
  stream: false,
});

console.log(response.choices[0].message.content);
console.log('Tokens used:', response.usage);
```

### Streaming (TypeScript)
```typescript
const stream = await client.chat.completions.create({
  model: 'asi1',
  messages: [{ role: 'user', content: 'Explain blockchain in simple terms' }],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? '');
}
```

### Web Search Enabled (TypeScript)
```typescript
const response = await client.chat.completions.create({
  model: 'asi1',
  messages: [{ role: 'user', content: 'Latest developments in AI research this week' }],
  // @ts-ignore — ASI:One extra body
  extra_body: { web_search: true },
});
```

### Agentic Session (TypeScript)
```typescript
import { v4 as uuidv4 } from 'uuid';

const sessionId = uuidv4();

const response = await client.chat.completions.create(
  {
    model: 'asi1',
    messages: [{ role: 'user', content: 'Check latest flight arrivals at Delhi airport' }],
    stream: true,
  },
  {
    headers: { 'x-session-id': sessionId },
  }
);

for await (const chunk of response) {
  if (chunk.choices[0]?.delta?.content) {
    process.stdout.write(chunk.choices[0].delta.content);
  }
}
```

---

## Accessing ASI:One-Specific Response Fields

```typescript
// Standard fields
console.log(response.choices[0].message.content); // Main answer
console.log(response.model);
console.log(response.usage);

// ASI:One fields — use type assertions
const raw = response as any;
if (raw.executable_data?.length) {
  console.log('Agent calls:', raw.executable_data);
}
if (raw.intermediate_steps?.length) {
  console.log('Reasoning steps:', raw.intermediate_steps);
}
if (raw.thought) {
  console.log('Model thought process:', raw.thought);
}
```

---

## LangChain Integration

### Setup
```bash
pip install langchain-openai  # Python
npm install @langchain/openai  # TypeScript
```

### Python — Basic
```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(
    model="asi1",
    base_url="https://api.asi1.ai/v1",
    api_key=os.getenv("ASI_ONE_API_KEY"),
    temperature=0.7,
)

response = llm.invoke([
    SystemMessage(content="You are a helpful AI assistant."),
    HumanMessage(content="What is agentic AI?")
])
print(response.content)
```

### Python — Streaming
```python
for chunk in llm.stream([HumanMessage(content="Explain blockchain")]):
    print(chunk.content, end="", flush=True)
```

### Python — Tool Calling
```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is sunny, 22°C"

@tool
def search_restaurants(city: str, cuisine: str) -> str:
    """Search for restaurants in a city by cuisine type."""
    return f"Found 5 {cuisine} restaurants in {city}"

llm_with_tools = llm.bind_tools([get_weather, search_restaurants])
response = llm_with_tools.invoke("What's the weather in Tokyo and find me sushi restaurants?")
print(response.tool_calls)
```

### Python — Session Persistence
```python
import uuid

session_id = str(uuid.uuid4())

llm_with_session = ChatOpenAI(
    model="asi1",
    base_url="https://api.asi1.ai/v1",
    api_key=os.getenv("ASI_ONE_API_KEY"),
    default_headers={"x-session-id": session_id},
)

r1 = llm_with_session.invoke([HumanMessage(content="My name is Alex and I'm planning a trip to Japan")])
r2 = llm_with_session.invoke([HumanMessage(content="What activities would you recommend for me?")])
# Model remembers context within session
```

### TypeScript — LangChain
```typescript
import { ChatOpenAI } from '@langchain/openai';
import { HumanMessage, SystemMessage } from '@langchain/core/messages';

const llm = new ChatOpenAI({
  model: 'asi1',
  openAIApiKey: process.env.ASI_ONE_API_KEY,
  configuration: { baseURL: 'https://api.asi1.ai/v1' },
  temperature: 0.7,
});

const response = await llm.invoke([
  new SystemMessage('You are a helpful assistant.'),
  new HumanMessage('What is agentic AI?'),
]);

console.log(response.content);
```

---

## Migrate from OpenAI — Diff

```typescript
// Before (OpenAI)
const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const r = await client.chat.completions.create({ model: 'gpt-4o', messages });

// After (ASI:One)
const client = new OpenAI({
  apiKey: process.env.ASI_ONE_API_KEY,
  baseURL: 'https://api.asi1.ai/v1', // ← only change!
});
const r = await client.chat.completions.create({ model: 'asi1', messages }); // ← model name
```

That's literally it for a basic migration. Add `x-session-id` header if you want agentic features.
