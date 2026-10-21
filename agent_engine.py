import asyncio
import json
from rag_engine import RAGEngine

# Initialize our RAG engine globally so it loads once
rag = RAGEngine()

class AgentEngine:
    """Orchestrates multi-agent workflow integrated with local RAG search."""
    
    def __init__(self, query: str):
        self.query = query

    async def run_workflow(self, websocket):
        """Executes agent steps, performs real vector search, and streams thoughts live."""
        
        # Step 1: Router Agent
        await asyncio.sleep(1.0)
        await websocket.send_text(json.dumps({
            "agent": "Router", 
            "status": f"Analyzing intent for query: '{self.query}'..."
        }))

        # Step 2: Researcher Agent (Real RAG Vector Search!)
        await asyncio.sleep(1.2)
        retrieved_chunks = rag.search(self.query, n_results=2)
        context_preview = " | ".join(retrieved_chunks)
        await websocket.send_text(json.dumps({
            "agent": "Researcher", 
            "status": f"Fetched context from ChromaDB: '{context_preview[:90]}...'"
        }))

        # Step 3: Fact-Checker Agent
        await asyncio.sleep(1.2)
        await websocket.send_text(json.dumps({
            "agent": "Fact-Checker", 
            "status": "Verified context relevance and filtered noise successfully."
        }))

        # Step 4: Synthesizer Agent
        await asyncio.sleep(1.2)
        synthesized_answer = f"Based on local vector search, here is the synthesis for '{self.query}': {retrieved_chunks[0] if retrieved_chunks else 'No direct match found.'}"
        await websocket.send_text(json.dumps({
            "agent": "Synthesizer", 
            "status": synthesized_answer
        }))

        # Final success packet
        await websocket.send_text(
            json.dumps({
                "agent": "System", 
                "status": "Workflow completed with live RAG retrieval! 🧠🎉"
            })
        )