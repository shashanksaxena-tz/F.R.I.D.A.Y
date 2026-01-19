from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt, context=None):
        """
        Generate a response based on the prompt and context.
        """
        pass

class MockLLM(LLMProvider):
    def generate(self, prompt, context=None):
        prompt = prompt.lower()
        if "hello" in prompt:
            return "Hello, Sir. All systems are online."
        elif "status" in prompt:
            return "Systems operational. Battery at 100%."
        elif "joke" in prompt:
            return "Why did the AI cross the road? To optimize the pathfinding algorithm."
        else:
            return f"I received your command: {prompt}. However, my language center is currently running in simulation mode."

class Brain:
    def __init__(self, provider: LLMProvider = None):
        self.provider = provider or MockLLM()

    def process(self, text):
        return self.provider.generate(text)
