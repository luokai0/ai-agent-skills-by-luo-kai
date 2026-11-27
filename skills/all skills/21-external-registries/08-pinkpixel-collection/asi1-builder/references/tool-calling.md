# Tool Calling — ASI:One

Tool calling lets ASI:One models invoke your custom functions. Supported on: `asi1-mini`, `asi1-fast`, `asi1-extended`.

---

## Tool Definition Schema

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Retrieves current weather for the given location.",
    "strict": true,
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "City and country e.g. Bogotá, Colombia"
        },
        "units": {
          "type": ["string", "null"],
          "enum": ["celsius", "fahrenheit"],
          "description": "Units the temperature will be returned in."
        }
      },
      "required": ["location", "units"],
      "additionalProperties": false
    }
  }
}
```

**Schema fields:**
- `name` — unique identifier (underscores/camelCase, no spaces)
- `description` — critical! model uses this to decide when to call the tool
- `parameters.type` — always `"object"`
- `properties` — each param with `type`, `description`, optional `enum`
- `required` — array of required param names
- `strict: true` — recommended; requires `additionalProperties: false` + all fields in `required`

---

## Complete Execution Cycle

### Step 1: Initial Request
```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.ASI_ONE_API_KEY!,
  baseURL: 'https://api.asi1.ai/v1',
});

const tools = [
  {
    type: 'function' as const,
    function: {
      name: 'get_weather',
      description: 'Get current temperature for a given location.',
      strict: true,
      parameters: {
        type: 'object',
        properties: {
          latitude: { type: 'number' },
          longitude: { type: 'number' },
        },
        required: ['latitude', 'longitude'],
        additionalProperties: false,
      },
    },
  },
];

const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
  { role: 'user', content: "What's the weather in London right now?" },
];

const response = await client.chat.completions.create({
  model: 'asi1-mini',
  messages,
  tools,
  temperature: 0.7,
  max_tokens: 1024,
});
```

### Step 2: Parse Tool Calls
```typescript
const firstMessage = response.choices[0].message;
const toolCalls = firstMessage.tool_calls ?? [];

// Add assistant message to history
messages.push(firstMessage);
```

### Step 3: Execute & Format Results
```typescript
async function getWeather(lat: number, lon: number): Promise<number> {
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m`;
  const res = await fetch(url);
  const data = await res.json();
  return data.current.temperature_2m;
}

for (const toolCall of toolCalls) {
  const args = JSON.parse(toolCall.function.arguments);
  let result: unknown;

  if (toolCall.function.name === 'get_weather') {
    const temp = await getWeather(args.latitude, args.longitude);
    result = { temperature_celsius: temp, location: `lat:${args.latitude}, lon:${args.longitude}` };
  } else {
    result = { error: `Unknown tool: ${toolCall.function.name}` };
  }

  // CRITICAL: content must be a JSON string, not an object
  messages.push({
    role: 'tool',
    tool_call_id: toolCall.id, // Use exact ID from tool call
    content: JSON.stringify(result),
  });
}
```

### Step 4: Send Results & Get Final Answer
```typescript
const finalResponse = await client.chat.completions.create({
  model: 'asi1-mini',
  messages,
  temperature: 0.7,
  max_tokens: 1024,
});

console.log(finalResponse.choices[0].message.content);
```

---

## Tool Choice Options

```typescript
// Auto (default) — model decides when/if to call tools
tool_choice: 'auto'

// Force at least one tool call
tool_choice: 'required'

// Force a specific tool
tool_choice: { type: 'function', function: { name: 'get_weather' } }

// No tools — pure text response
tool_choice: 'none'
```

---

## Parallel Tool Calling

By default, model may call multiple tools in one turn:

```typescript
// Disable parallel calls (one tool per turn max)
parallel_tool_calls: false
```

> Note: parallel tool calls may disable strict mode for those calls.

---

## Error Handling Pattern

```typescript
for (const toolCall of toolCalls) {
  let content: string;
  try {
    const result = await executeMyTool(toolCall.function.name, JSON.parse(toolCall.function.arguments));
    content = JSON.stringify(result);
  } catch (err) {
    content = JSON.stringify({
      error: `Tool execution failed: ${(err as Error).message}`,
      status: 'failed',
    });
  }

  messages.push({
    role: 'tool',
    tool_call_id: toolCall.id, // Still use original ID even on error
    content,
  });
}
```

---

## Message History Order (Critical)
1. Original user message
2. Assistant message with `tool_calls` (content null/empty — include as-is from response)
3. Tool result messages (`role: "tool"`, one per tool_call, matched by `tool_call_id`)

Violating this order causes errors.

---

## Python Example (Full Cycle)

```python
import requests, json

API_KEY = "your_api_key"
BASE_URL = "https://api.asi1.ai/v1"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

get_weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        }
    }
}

messages = [{"role": "user", "content": "What's the weather in London?"}]

# First call
r1 = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json={
    "model": "asi1-mini",
    "messages": messages,
    "tools": [get_weather_tool],
    "temperature": 0.7,
    "max_tokens": 1024
})
r1.raise_for_status()
r1_json = r1.json()

tool_calls = r1_json["choices"][0]["message"].get("tool_calls", [])
messages.append(r1_json["choices"][0]["message"])

def get_weather(lat, lon):
    r = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m")
    return r.json()["current"]["temperature_2m"]

for tc in tool_calls:
    args = json.loads(tc["function"]["arguments"])
    if tc["function"]["name"] == "get_weather":
        temp = get_weather(args["latitude"], args["longitude"])
        result = {"temperature_celsius": temp}
    else:
        result = {"error": f"Unknown: {tc['function']['name']}"}

    messages.append({
        "role": "tool",
        "tool_call_id": tc["id"],
        "content": json.dumps(result)
    })

# Final call
r2 = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json={
    "model": "asi1-mini",
    "messages": messages,
    "temperature": 0.7,
    "max_tokens": 1024
})
print(r2.json()["choices"][0]["message"]["content"])
```
