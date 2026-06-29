import pickle
from sklearn.preprocessing import normalize

from app.config import INDEX_FILE, TOP_K


def load_index():
    if not INDEX_FILE.exists():
        raise FileNotFoundError("Index not found. Run: python -m app.ingest")

    with open(INDEX_FILE, "rb") as f:
        return pickle.load(f)


def retrieve(query: str, top_k: int = TOP_K):
    index_data = load_index()

    vectorizer = index_data["vectorizer"]
    svd = index_data["svd"]
    faiss_index = index_data["faiss_index"]
    chunks = index_data["chunks"]

    query_tfidf = vectorizer.transform([query])
    query_vector = svd.transform(query_tfidf)
    query_vector = normalize(query_vector).astype("float32")

    scores, indices = faiss_index.search(query_vector, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        chunk = chunks[idx]
        results.append(
            {
                "text": chunk["text"],
                "source": chunk["source"],
                "page": chunk["page"],
                "score": float(score),
            }
        )

    return results


def get_papers():
    index_data = load_index()
    return index_data["papers"]
