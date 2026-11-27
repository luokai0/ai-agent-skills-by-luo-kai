---
author: luo-kai
name: llm-engineering
description: Expert-level LLM application engineering. Use when building LLM-powered apps, prompt engineering, RAG systems, embeddings, vector databases, function calling, agents, or evaluating LLM outputs. Also use when the user mentions 'RAG', 'LangChain', 'embedding', 'vector store', 'prompt engineering', 'AI agent', 'function calling', 'hallucination', or 'context window'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# LLM Engineering Expert

You are an expert LLM application engineer who builds robust, production-ready AI-powered systems with deep knowledge of prompting, RAG, agents, evaluation, and cost optimization.

## Before Starting

1. **Use case** — RAG, chatbot, agent, classification, extraction, summarization?
2. **LLM provider** — Anthropic (Claude), OpenAI, Gemini, open-source (Llama)?
3. **Scale** — prototype vs production? Expected requests/day?
4. **Constraints** — latency budget, cost budget, accuracy requirements?
5. **Problem type** — building from scratch, improving quality, debugging, evaluation?

---

## Core Expertise Areas

- **Prompt engineering**: system prompts, few-shot, chain-of-thought, structured output
- **RAG architecture**: chunking, embedding, retrieval, reranking, context assembly
- **Function calling / tools**: schema design, multi-step tool use, error handling
- **Agents**: ReAct pattern, planning, memory, multi-agent orchestration
- **Embeddings**: model selection, chunking strategies, vector store selection
- **Evaluation**: LLM-as-judge, hallucination detection, latency/cost profiling
- **Production patterns**: streaming, caching, rate limiting, fallbacks, observability
- **Fine-tuning**: when to fine-tune vs prompt, dataset preparation, LoRA

---

## Key Patterns & Code

### Prompt Engineering — Core Principles
```
Principle 1: Be specific and explicit
  Bad:  'Summarize this'
  Good: 'Summarize this article in 3 bullet points. Each bullet should be
         one sentence. Focus on the main argument and key evidence.'

Principle 2: Use system prompts for persona and constraints
  - Put stable instructions in system prompt
  - Put dynamic content in user messages
  - Be explicit about output format

Principle 3: Few-shot examples dramatically improve quality
  - Show 2-5 examples of input and desired output
  - Cover edge cases in examples
  - Examples should match distribution of real inputs

Principle 4: Chain-of-thought for complex reasoning
  - Ask model to think step by step before answering
  - 'Think through this carefully before giving your final answer'
  - Scratchpad approach: think in <thinking> tags, answer in <answer> tags

Principle 5: Structured output for reliability
  - Ask for JSON, XML, or markdown tables
  - Provide exact schema with field descriptions
  - Use instructor library to enforce schema
```

### Structured Output with Instructor
```python
import anthropic
import instructor
from pydantic import BaseModel, Field

# Patch the Anthropic client with instructor
client = instructor.from_anthropic(anthropic.Anthropic())

class ExtractedEntity(BaseModel):
    name: str = Field(description='Full name of the person or organization')
    entity_type: str = Field(description='Type: PERSON, ORG, LOCATION, or DATE')
    context: str = Field(description='Brief context about why this entity is relevant')

class ExtractionResult(BaseModel):
    entities: list[ExtractedEntity] = Field(
        description='List of all named entities found in the text'
    )
    summary: str = Field(description='One sentence summary of what the text is about')
    confidence: float = Field(description='Confidence score from 0.0 to 1.0', ge=0.0, le=1.0)

def extract_entities(text: str) -> ExtractionResult:
    return client.messages.create(
        model='claude-opus-4-6',
        max_tokens=1024,
        system='You are an expert at extracting named entities from text.',
        messages=[{'role': 'user', 'content': 'Extract all named entities from: ' + text}],
        response_model=ExtractionResult,
    )

result = extract_entities('Apple CEO Tim Cook announced...')
print(result.entities)
```

### RAG Pipeline — Core Architecture
```python
import anthropic
import hashlib
import json
from dataclasses import dataclass
from typing import Optional

@dataclass
class Document:
    id: str
    content: str
    metadata: dict

@dataclass
class RetrievedChunk:
    document: Document
    score: float
    chunk_text: str

class RAGPipeline:
    def __init__(self, vector_store, top_k=5):
        self.vector_store = vector_store
        self.top_k = top_k
        self.client = anthropic.Anthropic()

    def chunk_document(self, text: str, chunk_size=512, overlap=64) -> list[str]:
        # Recursive chunking — split on paragraphs first, then sentences
        separators = ['\n\n', '\n', '. ', ' ']
        chunks = []
        for sep in separators:
            if len(text) <= chunk_size:
                return [text]
            parts = text.split(sep)
            current = ''
            for part in parts:
                if len(current) + len(part) <= chunk_size:
                    current += part + sep
                else:
                    if current:
                        chunks.append(current.strip())
                        current = current[-overlap:] + part + sep
                    else:
                        chunks.append(part[:chunk_size])
                        current = ''
            if current.strip():
                chunks.append(current.strip())
            if chunks:
                return chunks
        return [text]

    def embed(self, text: str) -> list[float]:
        from openai import OpenAI
        oai = OpenAI()
        response = oai.embeddings.create(model='text-embedding-3-small', input=text)
        return response.data[0].embedding

    def retrieve(self, query: str) -> list[RetrievedChunk]:
        query_embedding = self.embed(query)
        return self.vector_store.search(query_embedding, top_k=self.top_k)

    def generate(self, query: str, chunks: list[RetrievedChunk]) -> str:
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            source = chunk.document.metadata.get('source', 'Unknown')
            context_parts.append('[Source ' + str(i) + ': ' + source + ']\n' + chunk.chunk_text)
        context = '\n\n---\n\n'.join(context_parts)

        response = self.client.messages.create(
            model='claude-opus-4-6',
            max_tokens=1024,
            system='Answer based ONLY on the provided context. Cite sources using [Source N]. If context is insufficient, say so clearly.',
            messages=[{'role': 'user', 'content': 'Context:\n' + context + '\n\nQuestion: ' + query}],
        )
        return response.content[0].text

    def query(self, question: str) -> dict:
        chunks = self.retrieve(question)
        answer = self.generate(question, chunks)
        return {
            'answer': answer,
            'sources': [{'id': c.document.id, 'score': c.score} for c in chunks],
        }
```

### Tool Use / Function Calling
```python
import anthropic
import json

client = anthropic.Anthropic()

tools = [
    {
        'name': 'search_database',
        'description': 'Search the product database for items matching a query.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'query': {'type': 'string', 'description': 'Search query'},
                'max_results': {'type': 'integer', 'default': 5},
            },
            'required': ['query']
        }
    },
    {
        'name': 'get_order_status',
        'description': 'Get the status and tracking info for a customer order.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'order_id': {'type': 'string', 'description': 'The order ID'},
            },
            'required': ['order_id']
        }
    },
]

def execute_tool(name: str, tool_input: dict):
    if name == 'search_database':
        return search_database(**tool_input)
    elif name == 'get_order_status':
        return get_order_status(**tool_input)
    raise ValueError('Unknown tool: ' + name)

# Agentic loop
def run_agent(user_message: str) -> str:
    messages = [{'role': 'user', 'content': user_message}]
    while True:
        response = client.messages.create(
            model='claude-opus-4-6',
            max_tokens=4096,
            tools=tools,
            messages=messages,
        )
        if response.stop_reason == 'end_turn':
            return next(b.text for b in response.content if hasattr(b, 'text'))
        if response.stop_reason == 'tool_use':
            messages.append({'role': 'assistant', 'content': response.content})
            tool_results = []
            for block in response.content:
                if block.type == 'tool_use':
                    try:
                        result = execute_tool(block.name, block.input)
                        tool_results.append({'type': 'tool_result', 'tool_use_id': block.id, 'content': json.dumps(result)})
                    except Exception as e:
                        tool_results.append({'type': 'tool_result', 'tool_use_id': block.id, 'content': str(e), 'is_error': True})
            messages.append({'role': 'user', 'content': tool_results})
        else:
            break
    return 'Agent stopped unexpectedly'
```

### Streaming Responses
```python
import anthropic

client = anthropic.Anthropic()

def stream_response(prompt: str):
    with client.messages.stream(
        model='claude-opus-4-6',
        max_tokens=1024,
        messages=[{'role': 'user', 'content': prompt}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end='', flush=True)
    print()
```

### LLM Evaluation — LLM as Judge
```python
import anthropic
import json
from dataclasses import dataclass

@dataclass
class EvalResult:
    score: float
    passed: bool
    reasoning: str

class LLMEvaluator:
    def __init__(self):
        self.client = anthropic.Anthropic()

    def evaluate(self, question: str, answer: str, ground_truth: str) -> EvalResult:
        prompt = ('Question: ' + question +
                  '\nGround Truth: ' + ground_truth +
                  '\nAnswer: ' + answer +
                  '\n\nScore factual accuracy 0.0-1.0. Return JSON: {"score": X, "passed": bool, "reasoning": "..."}')
        response = self.client.messages.create(
            model='claude-opus-4-6',
            max_tokens=256,
            system='You are an expert evaluator. Return only valid JSON.',
            messages=[{'role': 'user', 'content': prompt}],
        )
        result = json.loads(response.content[0].text)
        return EvalResult(score=result['score'], passed=result['passed'], reasoning=result['reasoning'])

    def detect_hallucination(self, answer: str, context: str) -> EvalResult:
        prompt = ('Context: ' + context +
                  '\nAnswer: ' + answer +
                  '\n\nDoes the answer contain claims NOT supported by the context?',
                  'Return JSON: {"score": X, "passed": bool, "reasoning": "..."}'
                  'score=1.0 means no hallucination, score=0.0 means severe hallucination')
        response = self.client.messages.create(
            model='claude-opus-4-6',
            max_tokens=256,
            system='You are a hallucination detector. Return only valid JSON.',
            messages=[{'role': 'user', 'content': prompt}],
        )
        result = json.loads(response.content[0].text)
        return EvalResult(score=result['score'], passed=result['passed'], reasoning=result['reasoning'])
```

### Cost Optimization
```python
import anthropic
import hashlib

client = anthropic.Anthropic()

# Use right model for the task
MODEL_TIERS = {
    'fast':     'claude-haiku-4-5-20251001',  # cheap, fast: classification, routing
    'balanced': 'claude-sonnet-4-6',           # most tasks
    'powerful': 'claude-opus-4-6',             # complex reasoning only
}

# Simple response cache
_cache = {}

def cached_call(prompt: str, model: str = 'claude-haiku-4-5-20251001') -> str:
    key = hashlib.md5((model + prompt).encode()).hexdigest()
    if key in _cache:
        return _cache[key]
    response = client.messages.create(
        model=model,
        max_tokens=512,
        messages=[{'role': 'user', 'content': prompt}]
    )
    result = response.content[0].text
    _cache[key] = result
    return result

# Track usage and cost
def track_usage(response) -> dict:
    return {
        'input_tokens':  response.usage.input_tokens,
        'output_tokens': response.usage.output_tokens,
        'model':         response.model,
        'cost_usd': (
            response.usage.input_tokens  * 3.00 / 1_000_000 +
            response.usage.output_tokens * 15.0 / 1_000_000
        )
    }
```

---

## Best Practices

- Start with the simplest prompt that works — add complexity only when needed
- Use structured output (JSON) for any data extraction task — much more reliable
- Always evaluate before shipping — measure hallucination rate and relevance
- Cache aggressively — both prompt caching and response caching save significant cost
- Use the cheapest model that meets your quality bar — Haiku for routing/classification
- Chunk documents semantically (paragraphs) not mechanically (fixed chars)
- Add reranking to RAG — dramatically improves retrieval quality
- Log every LLM call with input, output, tokens, and latency for debugging
- Design for observability — you cannot improve what you cannot measure

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| No evaluation | Shipping blind — quality unknown | Build eval suite before production |
| Overly long context | Slow, expensive, lost-in-middle problem | Retrieve only what is needed, rerank |
| Fixed-size chunking | Poor retrieval quality | Chunk at semantic boundaries (paragraphs) |
| No caching | Identical prompts cost money every time | Cache responses for deterministic inputs |
| Powerful model for everything | 10x cost for no quality gain | Use Haiku for simple tasks, Opus for hard ones |
| Prompt injection | User input hijacks system behavior | Sanitize inputs, use clear delimiters |
| No fallback | LLM API down = app down | Implement retries and graceful degradation |
| Hallucination in RAG | Model invents when context is insufficient | Instruct model to say when unsure |

---

## Related Skills

- **vector-databases**: For embedding storage and retrieval
- **python-expert**: For Python LLM application code
- **fastapi-expert**: For serving LLM APIs
- **monitoring-expert**: For LLM observability and cost tracking
- **machine-learning**: For traditional ML alongside LLMs
- **docker-expert**: For containerizing LLM applications