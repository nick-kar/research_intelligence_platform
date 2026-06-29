from rank_bm25 import BM25Okapi

from app.retriever import load_index
from app.semantic_index import semantic_search
from app.reranker import rerank_results


def tokenize(text: str):
    return text.lower().split()


def bm25_search(query: str, top_k: int = 10):
    index = load_index()
    chunks = index["chunks"]

    corpus = [tokenize(chunk["text"]) for chunk in chunks]
    bm25 = BM25Okapi(corpus)

    scores = bm25.get_scores(tokenize(query))
    ranked_indices = scores.argsort()[::-1][:top_k]

    results = []

    for idx in ranked_indices:
        chunk = chunks[idx]
        results.append(
            {
                "text": chunk["text"],
                "source": chunk["source"],
                "page": chunk["page"],
                "score": float(scores[idx]),
                "retriever": "bm25",
            }
        )

    return results


def hybrid_search(query: str, top_k: int = 8):
    semantic_results = semantic_search(query, top_k=top_k)
    bm25_results = bm25_search(query, top_k=top_k)

    combined = {}

    for result in semantic_results:
        key = (result["source"], result["page"], result["text"][:120])
        combined[key] = result
        combined[key]["retriever"] = "semantic"

    for result in bm25_results:
        key = (result["source"], result["page"], result["text"][:120])

        if key in combined:
            combined[key]["score"] += result["score"]
            combined[key]["retriever"] = "hybrid"
        else:
            combined[key] = result

    reranked = rerank_results(query, list(combined.values()))
    return reranked[:top_k]