import re
from agents.agent_core import SentientAgent

class TodoDetector:
    def __init__(self, agent: SentientAgent):
        self.agent = agent

    def detect(self, message_text, context):
        # Simple explicit check
        if re.search(r"\b(remind me|please|todo)\b", message_text, re.I):
            return f"Explicit TODO: {message_text}"
        # Fallback to LLM suggestion
        return self.agent.suggest(context, f"Create an action from: {message_text}")
