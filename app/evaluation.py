import time
import numpy as np

from app.hybrid_retriever import hybrid_search


def precision_at_k(retrieved_sources, relevant_sources, k=5):
    retrieved_k = retrieved_sources[:k]
    if not retrieved_k:
        return 0.0
    hits = sum(1 for source in retrieved_k if source in relevant_sources)
    return hits / k


def recall_at_k(retrieved_sources, relevant_sources, k=5):
    if not relevant_sources:
        return 0.0
    retrieved_k = retrieved_sources[:k]
    hits = sum(1 for source in retrieved_k if source in relevant_sources)
    return hits / len(relevant_sources)


def reciprocal_rank(retrieved_sources, relevant_sources):
    for rank, source in enumerate(retrieved_sources, start=1):
        if source in relevant_sources:
            return 1 / rank
    return 0.0


def ndcg_at_k(retrieved_sources, relevant_sources, k=5):
    retrieved_k = retrieved_sources[:k]
    dcg = 0.0

    for i, source in enumerate(retrieved_k):
        relevance = 1 if source in relevant_sources else 0
        dcg += relevance / np.log2(i + 2)

    ideal_hits = min(len(relevant_sources), k)
    idcg = sum(1 / np.log2(i + 2) for i in range(ideal_hits))

    if idcg == 0:
        return 0.0

    return dcg / idcg


def evaluate_query(query, relevant_sources, k=5):
    start = time.time()
    results = hybrid_search(query, top_k=k)
    latency = time.time() - start

    retrieved_sources = [result["source"] for result in results]

    return {
        "query": query,
        "precision_at_k": precision_at_k(retrieved_sources, relevant_sources, k),
        "recall_at_k": recall_at_k(retrieved_sources, relevant_sources, k),
        "mrr": reciprocal_rank(retrieved_sources, relevant_sources),
        "ndcg_at_k": ndcg_at_k(retrieved_sources, relevant_sources, k),
        "latency_seconds": latency,
        "retrieved_sources": retrieved_sources,
    }