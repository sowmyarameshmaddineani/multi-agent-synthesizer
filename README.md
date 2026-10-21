# 🧠 Live Multi-Agent Knowledge Synthesizer

A high-performance, asynchronous Multi-Agent RAG System built with **FastAPI**, **WebSockets**, **ChromaDB**, and **Sentence-Transformers**.

## ✨ Features
- **Real-Time Telemetry:** Streams agent thoughts live over WebSockets.
- **Autonomous Multi-Agent Pipeline:**
  - 🚦 **Router:** Intent classification & query parsing.
  - 🔍 **Researcher:** Semantic vector search via ChromaDB & local PDF ingestion.
  - 🛡️ **Fact-Checker:** Relevancy scoring & noise filtration.
  - 📝 **Synthesizer:** Multi-source contextual response generation.
- **Persistent Session Memory:** Context-aware multi-turn conversations.
- **Document Ingestion:** Automated PDF parsing using `pypdf`.

## 🛠️ Quickstart

1. **Install Dependencies:**
   ```bash
   pip install fastapi uvicorn chromadb sentence-transformers pypdf python-dotenv