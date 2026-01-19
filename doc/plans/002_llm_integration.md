# LLM Integration Strategy

## Goal
Replace simple keyword matching with a sophisticated Language Model to understand intent and context.

## Design

### The "Brain" Class
Located in `friday/core/brain.py`.

```python
class LLMProvider:
    def generate_response(self, user_input, context):
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key):
        ...

class LocalLLMProvider(LLMProvider):
    # Connects to OobaBooga or Llama.cpp via API
    ...
```

### Prompt Engineering
The System Prompt will define F.R.I.D.A.Y.'s personality.
- "You are FRIDAY, a highly advanced AI assistant."
- "You are concise, helpful, and slightly witty."
- "You have access to the following tools: [Gmail, Weather, News...]"

### Context Window
We need to maintain a conversation history.
- `state.py` will hold the last N messages.
- Vision context (e.g., "I see a coffee cup") should be injected into the prompt.

### Function Calling / Tool Use
We will implement a basic "ReAct" loop or use OpenAI's Function Calling API to let the LLM trigger `integrations`.
