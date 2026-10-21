class ConversationMemory:
    """Manages multi-turn conversation history and context for agent sessions."""
    
    def __init__(self):
        self.history = []

    def add_interaction(self, query: str, response: str):
        self.history.append({"query": query, "response": response})

    def get_recent_context(self, limit: int = 3) -> str:
        """Retrieves recent conversation history as formatted context string."""
        recent = self.history[-limit:]
        context_lines = []
        for turn in recent:
            context_lines.append(f"User: {turn['query']}\nSynthesizer: {turn['response']}")
        return "\n".join(context_lines)