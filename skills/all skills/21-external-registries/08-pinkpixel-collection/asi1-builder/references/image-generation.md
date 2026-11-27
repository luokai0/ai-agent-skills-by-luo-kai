# Image Generation — ASI:One

**Endpoint:** `POST https://api.asi1.ai/v1/image/generate`

Note: This is a **separate endpoint** from chat completions, not `/v1/chat/completions`.

---

## Request Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `prompt` | string | ✅ | — | Text description of image |
| `size` | string | ❌ | `"1024x1024"` | Image dimensions |
| `model` | string | ❌ | `"asi1-mini"` | Generation model |

## Supported Sizes

| Size | Orientation | Best For |
|---|---|---|
| `1024x1024` | Square | Avatars, general purpose, icons |
| `1792x1024` | Landscape | Banners, wallpapers, wide scenes |
| `1024x1792` | Portrait | Mobile wallpapers, tall content |

---

## Response Format

Returns base64-encoded PNG as a data URL:

```json
{
  "status": 1,
  "message": "Success",
  "created": 1753792957496,
  "images": [
    {
      "url": "data:image/png;base64,iVBORw0KGgoAAA..."
    }
  ]
}
```

---

## TypeScript Examples

### Basic Generation
```typescript
async function generateImage(prompt: string, size = '1024x1024'): Promise<string> {
  const response = await fetch('https://api.asi1.ai/v1/image/generate', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.ASI_ONE_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt, size, model: 'asi1-mini' }),
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(`Image gen failed: ${JSON.stringify(err)}`);
  }

  const data = await response.json();
  return data.images[0].url; // base64 data URL
}

// Usage
const imageUrl = await generateImage(
  'A futuristic city skyline at sunset with flying cars',
  '1792x1024'
);
```

### Save to File (Node.js)
```typescript
import { writeFileSync } from 'fs';

const dataUrl = await generateImage('A serene mountain lake at dawn');

// Strip the data URL prefix and decode
const base64 = dataUrl.replace(/^data:image\/\w+;base64,/, '');
const buffer = Buffer.from(base64, 'base64');
writeFileSync('output.png', buffer);
console.log('Saved to output.png');
```

### Display in Browser (React)
```tsx
function ImageDisplay({ prompt }: { prompt: string }) {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function generate() {
    setLoading(true);
    try {
      const res = await fetch('/api/generate-image', {
        method: 'POST',
        body: JSON.stringify({ prompt }),
        headers: { 'Content-Type': 'application/json' },
      });
      const data = await res.json();
      setImageUrl(data.url);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <button onClick={generate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Image'}
      </button>
      {imageUrl && <img src={imageUrl} alt={prompt} />}
    </div>
  );
}
```

---

## Python Examples

### Basic
```python
import requests, base64

def generate_image(prompt: str, size: str = "1024x1024") -> str:
    """Returns base64 data URL."""
    response = requests.post(
        "https://api.asi1.ai/v1/image/generate",
        headers={
            "Authorization": f"Bearer {os.getenv('ASI_ONE_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={"prompt": prompt, "size": size, "model": "asi1-mini"},
    )
    response.raise_for_status()
    return response.json()["images"][0]["url"]

# Save to disk
import base64, re
data_url = generate_image("A cyberpunk street at night", "1792x1024")
img_data = base64.b64decode(re.sub(r'^data:image/\w+;base64,', '', data_url))
with open("output.png", "wb") as f:
    f.write(img_data)
```

### Batch (Async)
```python
import asyncio, aiohttp, os

async def generate_multiple(prompts: list[str]) -> list[str]:
    API_KEY = os.getenv("ASI_ONE_API_KEY")
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        tasks = [
            session.post(
                "https://api.asi1.ai/v1/image/generate",
                headers=headers,
                json={"prompt": p, "size": "1024x1024"}
            )
            for p in prompts
        ]
        responses = await asyncio.gather(*tasks)
        results = []
        for resp in responses:
            data = await resp.json()
            results.append(data["images"][0]["url"])
        return results

# Usage
prompts = [
    "A cyberpunk city at night",
    "A peaceful forest with morning mist",
    "A futuristic spaceship in orbit",
]
images = asyncio.run(generate_multiple(prompts))
```

---

## Prompt Writing Tips

| ❌ Weak | ✅ Strong |
|---|---|
| "mountains" | "A misty mountain valley at dawn with golden sunlight filtering through pine trees, photorealistic" |
| "person" | "A professional headshot of a confident businesswoman in a modern office setting, natural lighting" |
| "abstract art" | "A vibrant abstract painting with swirling blues and oranges in the style of Van Gogh, oil texture" |

**Include:** style, mood, lighting, perspective, colors, textures, composition details.

---

## Error Responses

```json
{
  "error": {
    "message": "Invalid prompt provided",
    "type": "invalid_request_error",
    "code": 400
  }
}
```

| Status | Meaning |
|---|---|
| 400 | Bad request / invalid params |
| 401 | Invalid or missing API key |
| 404 | Endpoint not found |
| 500 | Server error |

Always implement exponential backoff for retries.

---

## Also via Agentic LLM

You can also generate images through the agentic endpoint by mentioning a specific model in your prompt:

```python
# Using asi1 to generate via Agentverse agents
response = client.chat.completions.create(
    model="asi1",
    messages=[{
        "role": "user",
        "content": "use Hi-dream model to generate image of a monkey sitting on top of a mountain"
    }],
    stream=True,
    extra_headers={"x-session-id": session_id}
)
# Response will include a hosted image URL in the content
```
