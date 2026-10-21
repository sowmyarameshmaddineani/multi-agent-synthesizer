import chromadb
from sentence_transformers import SentenceTransformer

class RAGEngine:
    def __init__(self):
        # 1. Initialize a local ChromaDB client (stored locally in a folder named 'chroma_db')
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # 2. Load a lightweight, high-performance sentence embedding model
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        
        # 3. Get or create a collection for our knowledge base
        self.collection = self.client.get_or_create_collection(name="knowledge_base")
        
        # Add some initial default knowledge if the collection is empty
        if self.collection.count() == 0:
            self.seed_initial_data()

    def seed_initial_data(self):
        """Seeds the vector database with starter documentation."""
        docs = [
            "Quantum computing leverages quantum mechanics principles like superposition and entanglement to process complex data exponentially faster than classical computers.",
            "FastAPI is a modern, high-performance web framework for building APIs with Python based on standard type hints.",
            "Retrieval-Augmented Generation (RAG) improves LLM responses by fetching relevant factual context from an external vector database before generating text.",
            "WebSockets enable bi-directional, real-time communication channels over a single TCP connection between a client and a server."
        ]
        ids = ["doc1", "doc2", "doc3", "doc4"]
        
        # Generate embeddings and add to ChromaDB
        embeddings = self.encoder.encode(docs).tolist()
        self.collection.add(
            documents=docs,
            embeddings=embeddings,
            ids=ids
        )
        print("Successfully seeded initial knowledge base into ChromaDB!")

    def search(self, query: str, n_results: int = 2):
        """Searches the vector database for context chunks most relevant to the query."""
        query_embedding = self.encoder.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        # Extract the retrieved text chunks
        return results["documents"][0] if results["documents"] else []