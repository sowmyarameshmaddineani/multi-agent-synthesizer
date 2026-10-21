import os
from pathlib import Path
from pypdf import PdfReader
from rag_engine import RAGEngine

class DocumentIngester:
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.rag = RAGEngine()

    def process_pdf(self, file_path: Path) -> list:
        """Extracts text from a PDF file and splits it into chunked segments."""
        reader = PdfReader(file_path)
        chunks = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                # Clean and split text into manageable chunks (~500 characters with a small overlap)
                cleaned_text = " ".join(text.split())
                chunk_size = 500
                for j in range(0, len(cleaned_text), chunk_size):
                    chunk = cleaned_text[j:j + chunk_size]
                    chunks.append({
                        "id": f"{file_path.name}_page{i}_chunk{j}",
                        "text": chunk,
                        "source": file_path.name
                    })
        return chunks

    def ingest_directory(self):
        """Scans the data directory, processes files, and adds them to ChromaDB."""
        if not self.data_dir.exists():
            print(f"Directory {self.data_dir} does not exist. Creating it now...")
            self.data_dir.mkdir(parents=True, exist_ok=True)
            print("Please drop some PDF files inside the './data' folder and run this script again!")
            return

        pdf_files = list(self.data_dir.glob("*.pdf"))
        if not pdf_files:
            print(f"No PDF files found in {self.data_dir}. Add a PDF and re-run ingestion.")
            return

        total_added = 0
        for pdf_path in pdf_files:
            print(f"Processing PDF: {pdf_path.name}...")
            chunks = self.process_pdf(pdf_path)
            
            if chunks:
                documents = [c["text"] for c in chunks]
                ids = [c["id"] for c in chunks]
                metadatas = [{"source": c["source"]} for c in chunks]
                
                # Generate embeddings and push to ChromaDB collection
                embeddings = self.rag.encoder.encode(documents).tolist()
                self.rag.collection.add(
                    documents=documents,
                    embeddings=embeddings,
                    ids=ids,
                    metadatas=metadatas
                )
                total_added += len(documents)
                print(f"Successfully ingested {len(documents)} chunks from {pdf_path.name}!")

        print(f"Ingestion complete! Total new chunks added: {total_added}")

if __name__ == "__main__":
    ingester = DocumentIngester()
    ingester.ingest_directory()