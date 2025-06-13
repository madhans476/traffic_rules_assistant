# src/retriever.py

import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, index_path: str, chunk_json_path: str, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the Retriever with FAISS index, chunk texts, and embedding model.
        """
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index not found at {index_path}")
        if not os.path.exists(chunk_json_path):
            raise FileNotFoundError(f"Chunk file not found at {chunk_json_path}")

        self.index = faiss.read_index(index_path)
        self.chunks = self._load_chunks(chunk_json_path)
        self.model = SentenceTransformer(model_name)

    def _load_chunks(self, json_path: str) -> list[dict]:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def query(self, question: str, top_k: int = 3) -> list[dict]:
        """
        Takes a user question and returns top_k relevant chunks.
        """
        question_embedding = self.model.encode([question])
        D, I = self.index.search(np.array(question_embedding), top_k)
        
        results = []
        for idx in I[0]:
            if idx < len(self.chunks):
                results.append(self.chunks[idx])
        return results

# For testing this module independently
if __name__ == "__main__":
    # base_dir = os.path.join("..", "data", "processed")
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    retriever = Retriever(
            index_path=os.path.join(BASE_DIR, "data", "processed", "faiss_cosine_index.idx"),
            chunk_json_path=os.path.join(BASE_DIR, "data", "processed", "TN_traffic_rules_chunks.json")
    )

    query = "What is the fine for not wearing a helmet?"
    top_chunks = retriever.query(query, top_k=10)

    print("\nTop Matching Chunks:\n")
    for i, chunk in enumerate(top_chunks, 1):
        print(f"[Chunk {chunk['chunk_id']}]\n{chunk['text']}\n{'-'*60}")
