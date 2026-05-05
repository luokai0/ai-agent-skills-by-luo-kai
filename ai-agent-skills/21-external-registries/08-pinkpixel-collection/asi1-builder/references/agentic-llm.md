# Agentic LLM — ASI:One

The `asi1` model autonomously discovers and coordinates agents from the [Agentverse marketplace](https://agentverse.ai/) to complete complex, multi-step tasks. It handles agent selection, orchestration, and planning on its own.

---

## Key Concepts

- **Agentverse**: marketplace of specialized AI agents (weather, flights, scheduling, research, image gen, etc.)
- **Session ID**: a UUID you generate and pass as `x-session-id` header — maintains context across turns
- **Deferred responses**: some Agentverse agents take time; you poll until the response updates
- **Streaming**: use for better UX during long agentic tasks

---

## Session Management

Always generate a UUID session ID and include it in every request for agentic workflows:

### TypeScript
```typescript
import { v4 as uuidv4 } from 'uuid';
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.ASI_ONE_API_KEY!,
  baseURL: 'https://api.asi1.ai/v1',
});

// In production: store session IDs in Redis/DB keyed by user/conversation ID
const sessionMap = new Map<string, string>();

function getSessionId(conversationId: string): string {
  if (!sessionMap.has(conversationId)) {
    sessionMap.set(conversationId, uuidv4());
  }
  return sessionMap.get(conversationId)!;
}

async function ask(conversationId: string, messages: OpenAI.Chat.ChatCompletionMessageParam[]) {
  const sessionId = getSessionId(conversationId);

  const response = await client.chat.completions.create(
    {
      model: 'asi1',
      messages,
      stream: false,
    },
    {
      headers: { 'x-session-id': sessionId },
    }
  );

  return response.choices[0].message.content;
}
```

### Streaming with Session
```typescript
async function askStreaming(conversationId: string, messages: OpenAI.Chat.ChatCompletionMessageParam[]) {
  const sessionId = getSessionId(conversationId);
  let fullText = '';

  const stream = await client.chat.completions.create(
    {
      model: 'asi1',
      messages,
      stream: true,
    },
    {
      headers: { 'x-session-id': sessionId },
    }
  );

  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content;
    if (content) {
      process.stdout.write(content);
      fullText += content;
    }
  }

  return fullText;
}
```

---

## Async / Deferred Agent Polling

Some Agentverse agents run asynchronous workflows. When they do, the initial response might be something like "I've sent the request" — then you poll for updates:

```typescript
async function pollForUpdate(
  conversationId: string,
  history: OpenAI.Chat.ChatCompletionMessageParam[],
  options = { intervalMs: 5000, maxAttempts: 24 } // ~2 min
): Promise<string | null> {
  const lastContent = (history[history.length - 1] as any).content as string;

  for (let i = 0; i < options.maxAttempts; i++) {
    await new Promise(r => setTimeout(r, options.intervalMs));
    console.log(`Polling attempt ${i + 1}...`);

    const update = await ask(conversationId, [
      ...history,
      { role: 'user', content: 'Any update?' }
    ]);

    if (update && update.trim() !== lastContent.trim()) {
      return update; // New content = task completed
    }
  }

  return null; // Timed out
}

// Usage
const convId = uuidv4();
const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
  { role: 'user', content: 'Check the latest flight arrivals at Delhi airport' }
];

const reply = await ask(convId, messages);
history.push({ role: 'assistant', content: reply! });

// If the reply sounds like a deferred ack, poll
if (reply?.includes("sent") || reply?.includes("checking")) {
  const result = await pollForUpdate(convId, history);
  console.log('Agent result:', result);
}
```

---

## Python Full Example

```python
import os, uuid, json, requests, sys, time

API_KEY = os.getenv("ASI_ONE_API_KEY") or "sk-REPLACE_ME"
ENDPOINT = "https://api.asi1.ai/v1/chat/completions"
MODEL = "asi1"
TIMEOUT = 90

SESSION_MAP: dict[str, str] = {}

def get_session_id(conv_id: str) -> str:
    if conv_id not in SESSION_MAP:
        SESSION_MAP[conv_id] = str(uuid.uuid4())
    return SESSION_MAP[conv_id]

def ask(conv_id: str, messages: list[dict], *, stream: bool = False) -> str:
    session_id = get_session_id(conv_id)
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "x-session-id": session_id,
        "Content-Type": "application/json",
    }
    payload = {"model": MODEL, "messages": messages, "stream": stream}

    if not stream:
        resp = requests.post(ENDPOINT, headers=headers, json=payload, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    # Streaming
    with requests.post(ENDPOINT, headers=headers, json=payload, timeout=TIMEOUT, stream=True) as resp:
        resp.raise_for_status()
        full_text = ""
        for line in resp.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data: "):
                continue
            line = line[len("data: "):]
            if line == "[DONE]":
                break
            try:
                chunk = json.loads(line)
                choices = chunk.get("choices")
                if choices and "content" in choices[0].get("delta", {}):
                    token = choices[0]["delta"]["content"]
                    sys.stdout.write(token)
                    sys.stdout.flush()
                    full_text += token
            except json.JSONDecodeError:
                continue
        print()
        return full_text

def poll_for_update(conv_id, history, wait_sec=5, max_attempts=24):
    last = history[-1]["content"]
    for attempt in range(max_attempts):
        time.sleep(wait_sec)
        print(f"Polling {attempt + 1}...")
        update = ask(conv_id, history + [{"role": "user", "content": "Any update?"}])
        if update and update.strip() != last.strip():
            return update
    return None

# Example
if __name__ == "__main__":
    conv_id = str(uuid.uuid4())
    messages = [{"role": "user", "content": "Generate an image of a futuristic city using the Hi-dream model"}]
    reply = ask(conv_id, messages, stream=True)
    print(f"\nReply: {reply}")
```

---

## Best Practices

| Topic | Guidance |
|---|---|
| Session IDs | Use UUIDs, store in Redis/DB for production |
| Always include | `x-session-id` header on every request in a conversation |
| Be specific | Detailed prompts help agent discovery (e.g., "book me a flight from London to Tokyo on June 5th") |
| Async tasks | Implement polling — Agentverse agents may take 30–90 seconds |
| Streaming | Use it for better UX on long-running tasks |
| Timeout | Set to 90+ seconds for complex agentic workflows |
| Error handling | Implement exponential backoff for network failures |

---

## Directly Targeting an Agentverse Agent

If you know the agent's address, target it directly:

```typescript
const response = await client.chat.completions.create({
  model: 'asi1',
  messages: [{ role: 'user', content: 'Get weather for San Francisco' }],
  // @ts-ignore
  agent_address: 'agent1qde95qr0dzcnhhs8f65hkwujn9mh89jx0u7u7g6nv3tm2jxvjwhkunvessq',
});
```

Or mention an agent in your prompt:
```
@agent1qde95qr0... please get me the weather for San Francisco
```
