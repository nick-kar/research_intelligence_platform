import pickle
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

from app.retriever import load_index
from app.config import VECTOR_STORE_DIR

SEMANTIC_INDEX_FILE = VECTOR_STORE_DIR / "semantic_index.pkl"
DEFAULT_MODEL = "all-MiniLM-L6-v2"


def build_semantic_index(model_name: str = DEFAULT_MODEL):
    index_data = load_index()
    chunks = index_data["chunks"]

    texts = [chunk["text"] for chunk in chunks]

    model = SentenceTransformer(model_name)
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True,
        normalize_embeddings=True,
    ).astype("float32")

    faiss_index = faiss.IndexFlatIP(embeddings.shape[1])
    faiss_index.add(embeddings)

    semantic_data = {
        "model_name": model_name,
        "faiss_index": faiss_index,
        "chunks": chunks,
        "embedding_dim": embeddings.shape[1],
    }

    with open(SEMANTIC_INDEX_FILE, "wb") as file:
        pickle.dump(semantic_data, file)

    print(f"Built semantic index with {len(chunks)} chunks.")
    print(f"Embedding dimension: {embeddings.shape[1]}")
    print(f"Model: {model_name}")


def load_semantic_index():
    if not SEMANTIC_INDEX_FILE.exists():
        raise FileNotFoundError(
            "Semantic index not found. Run: python -m app.semantic_index"
        )

    with open(SEMANTIC_INDEX_FILE, "rb") as file:
        return pickle.load(file)


def semantic_search(query: str, top_k: int = 8):
    semantic_data = load_semantic_index()

    model = SentenceTransformer(semantic_data["model_name"])
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    scores, indices = semantic_data["faiss_index"].search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        chunk = semantic_data["chunks"][idx]

        results.append(
            {
                "text": chunk["text"],
                "source": chunk["source"],
                "page": chunk["page"],
                "score": float(score),
                "retriever": "semantic",
            }
        )

    return results


if __name__ == "__main__":
    build_semantic_index()