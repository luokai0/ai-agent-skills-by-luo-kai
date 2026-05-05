# Agent Chat Protocol — ASI:One / uAgents

The Agent Chat Protocol enables AI agents built with the `uagents` library to communicate in natural language, interoperate with Agentverse, and chain together using structured outputs. This is **Python-only** (uagents SDK).

---

## Install

```bash
pip install uagents requests
```

---

## Core Concepts

- **Agent**: runtime that sends/receives protocol-compliant messages
- **Chat Protocol**: standard schema for `ChatMessage`, `ChatAcknowledgement`, session start/end
- **Structured Output Protocol**: request JSON from another AI agent
- **Session**: storage for cross-message state (`ctx.storage.set/get`)
- **Hosted vs Local**: agents can run locally or be hosted on Agentverse

---

## Protocol Imports

```python
from uagents import Agent, Context, Protocol, Model
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    chat_protocol_spec,
    StartSessionContent,
    EndSessionContent,
)
from datetime import datetime
from uuid import uuid4
from typing import Any, Dict
```

---

## Structured Output Models

```python
class StructuredOutputPrompt(Model):
    prompt: str
    output_schema: Dict[str, Any]

class StructuredOutputResponse(Model):
    output: Dict[str, Any]
```

---

## Helper: Create Chat Message

```python
def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )
```

---

## Complete Weather Agent Example

### `agents.py` (main agent)

```python
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement, ChatMessage, TextContent,
    chat_protocol_spec, StartSessionContent, EndSessionContent,
)
from functions import get_weather, WeatherRequest
from datetime import datetime
from uuid import uuid4
from typing import Any, Dict
from uagents import Model

class StructuredOutputPrompt(Model):
    prompt: str
    output_schema: Dict[str, Any]

class StructuredOutputResponse(Model):
    output: Dict[str, Any]

# Address of the OpenAI-backed AI agent on Agentverse
AI_AGENT_ADDRESS = "agent1qtlpfshtlcxekgrfcpmv7m9zpajuwu7d5jfyachvpa4u3dkt6k0uwwp2lct"

agent = Agent()
chat_proto = Protocol(spec=chat_protocol_spec)
struct_output_client_proto = Protocol(name="StructuredOutputClientProtocol", version="0.1.0")

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=content)

@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Got message from {sender}")
    ctx.storage.set(str(ctx.session), sender)  # Remember sender for this session

    # Acknowledge receipt
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.utcnow(),
        acknowledged_msg_id=msg.msg_id
    ))

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started by {sender}")
            continue
        elif isinstance(item, TextContent):
            ctx.logger.info(f"User said: {item.text}")
            # Forward to AI agent for structured output extraction
            await ctx.send(AI_AGENT_ADDRESS, StructuredOutputPrompt(
                prompt=item.text,
                output_schema=WeatherRequest.schema()
            ))
        else:
            ctx.logger.info("Ignoring non-text content")

@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Ack from {sender} for {msg.acknowledged_msg_id}")

@struct_output_client_proto.on_message(StructuredOutputResponse)
async def handle_structured_output(ctx: Context, sender: str, msg: StructuredOutputResponse):
    session_sender = ctx.storage.get(str(ctx.session))
    if not session_sender:
        ctx.logger.error("No session sender in storage")
        return

    if "<UNKNOWN>" in str(msg.output):
        await ctx.send(session_sender, create_text_chat(
            "Sorry, I couldn't process your location request. Please try again."
        ))
        return

    try:
        location = msg.output.get("location") if isinstance(msg.output, dict) else None
        if not location:
            raise ValueError("No location in structured output")
        weather = get_weather(location)
    except Exception as err:
        ctx.logger.error(f"Error: {err}")
        await ctx.send(session_sender, create_text_chat(
            "Sorry, I couldn't get the weather. Please try again."
        ))
        return

    if "error" in weather:
        await ctx.send(session_sender, create_text_chat(str(weather["error"])))
        return

    reply = weather.get("weather") or f"Weather for {location}: (no data)"
    await ctx.send(session_sender, create_text_chat(reply))

agent.include(chat_proto, publish_manifest=True)
agent.include(struct_output_client_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
```

### `functions.py` (utilities)

```python
from uagents import Model
import requests

class WeatherRequest(Model):
    location: str

class WeatherResponse(Model):
    weather: str

def get_weather(location: str) -> dict:
    """Return current weather for a location string like 'Paris, France'."""
    if not location or not location.strip():
        raise ValueError("location is required")

    # Geocode
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": location, "count": 1, "language": "en", "format": "json"},
        timeout=60,
    )
    geo.raise_for_status()
    g = geo.json()
    if not g.get("results"):
        raise RuntimeError(f"No geocoding match for: {location}")

    r0 = g["results"][0]
    lat, lon = r0["latitude"], r0["longitude"]
    tz = r0.get("timezone") or "auto"
    display = ", ".join(v for v in [r0.get("name"), r0.get("admin1"), r0.get("country")] if v)

    # Fetch weather
    wx = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat, "longitude": lon, "timezone": tz,
            "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m",
        },
        timeout=60,
    )
    wx.raise_for_status()
    current = wx.json().get("current", {})

    parts = [f"Weather for {display}"]
    if (t := current.get("temperature_2m")) is not None:
        parts.append(f"temp {t}°C")
    if (a := current.get("apparent_temperature")) is not None:
        parts.append(f"feels like {a}°C")
    if (h := current.get("relative_humidity_2m")) is not None:
        parts.append(f"RH {h}%")
    if (w := current.get("wind_speed_10m")) is not None:
        parts.append(f"wind {w} km/h")

    return {"weather": ", ".join(parts)}
```

---

## Protocol Flow Diagram

```
User
  │
  ▼
[ChatMessage] ──► Your Agent
                    │ ack back to user
                    │ forward StructuredOutputPrompt ──► AI Agent (Agentverse)
                    │                                         │
                    │         StructuredOutputResponse ◄──────┘
                    │ (parse JSON, call external API)
                    │
                    ▼
                [ChatMessage reply] ──► User
```

---

## Key Protocol Rules

1. **Always ack** incoming `ChatMessage` immediately with `ChatAcknowledgement`
2. **Store session sender** in `ctx.storage.set(str(ctx.session), sender)` so you can reply later
3. **Retrieve sender** when handling async responses: `ctx.storage.get(str(ctx.session))`
4. **Handle `<UNKNOWN>`** — the AI agent returns this when it can't extract the structured field
5. **Include both protocols** with `publish_manifest=True` so they're discoverable on Agentverse
6. **Session is per-connection** — `ctx.session` gives a unique ID per conversation

---

## Hosted vs Local Agents

**Local:**
```bash
python agents.py
```

**Hosted on Agentverse:**
- Create agent at https://agentverse.ai/
- Upload code files
- Agent gets a permanent address like `agent1q...`
- Accessible from ASI:One via `@agent1q...` mentions or `agent_address` param

---

## Calling from ASI:One Chat

Once your agent is on Agentverse, call it directly from ASI:One:

```python
# In a normal ASI:One chat
response = client.chat.completions.create(
    model="asi1",
    messages=[{
        "role": "user",
        "content": "@agent1qde95qr0dzcnhhs8f65hkwujn9mh89jx0u7u7g6nv3tm2jxvjwhkunvessq please get me weather for San Francisco"
    }],
    extra_headers={"x-session-id": session_id},
)
```

---

## Why Use Agent Chat Protocol?

| Benefit | Details |
|---|---|
| Natural language | Users type naturally; protocol handles structure |
| Interoperable | Any agent implementing the spec can communicate |
| Extensible | Add more client protocols (structured output, etc.) |
| Reliable | Acks + session controls for robust UX |
| Agentverse-native | Agents discoverable and orchestratable by ASI:One |
