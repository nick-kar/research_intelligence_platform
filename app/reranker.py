def rerank_results(query: str, results):
    """
    Lightweight reranker based on lexical overlap and retrieval score.
    """
    query_terms = set(query.lower().split())
    reranked = []

    for result in results:
        text_terms = set(result["text"].lower().split())
        overlap = len(query_terms.intersection(text_terms))

        base_score = result.get("score", 0.0)
        rerank_score = base_score + 0.05 * overlap

        updated = result.copy()
        updated["rerank_score"] = rerank_score
        reranked.append(updated)

    return sorted(reranked, key=lambda item: item["rerank_score"], reverse=True)