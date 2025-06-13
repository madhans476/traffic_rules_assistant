import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def load_chunks(json_path: str):
    """Loads text chunks from a JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_embeddings(texts: list[str], model_name='all-MiniLM-L6-v2') -> np.ndarray:
    """Generates embeddings using a pre-trained SentenceTransformer."""
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=True)
    return np.array(embeddings)

def save_faiss_index(embeddings: np.ndarray, output_path: str):
    """Saves normalized embeddings to a FAISS index file using cosine similarity."""
    # Normalize embeddings to unit length
    faiss.normalize_L2(embeddings)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    faiss.write_index(index, output_path)
    print(f"FAISS index (cosine similarity) saved to {output_path}")


if __name__ == "__main__":
    chunk_path = os.path.join("..", "data", "processed", "TN_traffic_rules_chunks.json")
    index_path = os.path.join("..", "data", "processed", "faiss_cosine_index.idx")

    chunks = load_chunks(chunk_path)
    texts = [chunk["text"] for chunk in chunks]

    embeddings = generate_embeddings(texts)
    save_faiss_index(embeddings, index_path)
