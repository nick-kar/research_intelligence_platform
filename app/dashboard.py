from collections import Counter


def build_dashboard_stats(papers, chunks):
    keyword_counter = Counter()

    for paper in papers:
        keyword_counter.update(paper.get("keywords", []))

    return {
        "num_papers": len(papers),
        "num_chunks": len(chunks),
        "total_pages": sum(p.get("num_pages", 0) for p in papers),
        "top_keywords": keyword_counter.most_common(15),
    }
