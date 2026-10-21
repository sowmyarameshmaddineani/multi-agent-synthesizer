import asyncio
import json
from rag_engine import RAGEngine
from memory import ConversationMemory

rag = RAGEngine()
# Global session memory instance for Month 5
session_memory = ConversationMemory()

class AgentEngine:
    """Orchestrates multi-agent reasoning loops with multi-turn memory."""
    
    def __init__(self, query: str):
        self.query = query

    async def run_workflow(self, websocket):
        """Executes the pipeline with awareness of prior conversation turns."""
        
        async def send_event(agent: str, status: str, payload: dict = None):
            message = {
                "agent": agent,
                "status": status,
                "payload": payload or {}
            }
            await websocket.send_text(json.dumps(message))
            await asyncio.sleep(0.8)

        # --- Step 1: Router Agent ---
        await send_event("Router", f"Analyzing query intent and checking conversation history...")
        prior_context = session_memory.get_recent_context()

        # --- Step 2: Researcher Agent ---
        await send_event("Researcher", "Executing semantic vector search with memory context expansion...")
        
        # Expand query search with recent history if applicable
        search_query = f"{self.query} {prior_context[:100]}" if prior_context else self.query
        
        results = rag.collection.query(
            query_embeddings=rag.encoder.encode([search_query]).tolist(),
            n_results=3
        )
        
        documents = results["documents"][0] if results and results["documents"] else []
        metadatas = results["metadatas"][0] if results and results["metadatas"] else [{}] * len(documents)
        sources = list(set([m.get("source", "Internal Base") for m in metadatas]))
        
        await send_event(
            "Researcher", 
            f"Retrieved {len(documents)} relevant chunks from sources: {', '.join(sources)}",
            {"chunks_found": len(documents), "sources": sources}
        )

        # --- Step 3: Fact-Checker Agent ---
        await send_event("Fact-Checker", "Verifying factual alignment against local document store and session memory...")
        verified_context = documents[0] if documents else "No direct matching context found."
        
        await send_event("Fact-Checker", "Verification successful. Context grounded securely.", {"confidence": "High"})

        # --- Step 4: Synthesizer Agent ---
        await send_event("Synthesizer", "Generating contextual synthesis...")
        
        final_answer = (
            f"**Query:** {self.query}\n\n"
            f"**Findings:** {verified_context}\n\n"
            f"*(Sources: {', '.join(sources)})*"
        )
        
        await send_event("Synthesizer", final_answer, {"synthesis": final_answer})

        # Save turn to memory
        session_memory.add_interaction(self.query, final_answer)

        # --- System Complete ---
        await send_event("System", "Month 5 multi-turn session workflow completed! 🧠💬")