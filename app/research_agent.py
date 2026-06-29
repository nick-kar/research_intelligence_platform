from app.citation_graph import graph_summary, create_interactive_graph
from app.retriever import retrieve, get_papers, load_index
from app.literature import build_literature_review
from app.gap_analysis import analyze_research_gaps
from app.dashboard import build_dashboard_stats
from app.citation_graph import graph_summary


class ResearchAgent:
    def answer_question(self, question: str):
        results = retrieve(question)

        if not results:
            return "No relevant evidence found.", []

        evidence = []

        for result in results:
            evidence.append(
                f"Source: {result['source']} | Page: {result['page']} | Score: {result['score']:.3f}\n"
                f"{result['text']}"
            )

        answer = (
            "# Grounded Research Answer\n\n"
            f"## Question\n{question}\n\n"
            "## Retrieved Evidence\n\n"
            + "\n\n---\n\n".join(evidence)
        )

        sources = [(r["source"], r["page"]) for r in results]
        return answer, sources

    def literature_review(self, topic: str):
        results = retrieve(topic, top_k=10)
        review = build_literature_review(topic, results)
        sources = [(r["source"], r["page"]) for r in results]
        return review, sources

    def compare_topics(self, topic_a: str, topic_b: str):
        results_a = retrieve(topic_a, top_k=5)
        results_b = retrieve(topic_b, top_k=5)

        text_a = "\n\n".join(
            [f"- {r['text'][:450]}... [{r['source']}, p. {r['page']}]" for r in results_a]
        )

        text_b = "\n\n".join(
            [f"- {r['text'][:450]}... [{r['source']}, p. {r['page']}]" for r in results_b]
        )

        comparison = (
            f"# Research Topic Comparison\n\n"
            f"## Topic A: {topic_a}\n{text_a}\n\n"
            f"## Topic B: {topic_b}\n{text_b}\n\n"
            "## Interpretation\n"
            "The retrieved evidence can be compared across methodology, assumptions, limitations, applications, and future directions."
        )

        sources = [(r["source"], r["page"]) for r in results_a + results_b]
        return comparison, sources

    def research_gap_analysis(self, topic: str):
        results = retrieve(topic, top_k=10)
        gaps = analyze_research_gaps(topic, results)
        sources = [(r["source"], r["page"]) for r in results]
        return gaps, sources

    def paper_inventory(self):
        papers = get_papers()

        lines = []
        for paper in papers:
            lines.append(
                f"- **{paper['filename']}** | Pages: {paper['num_pages']} | Keywords: {', '.join(paper['keywords'])}"
            )

        return "# Indexed Papers\n\n" + "\n".join(lines)

    def dashboard_stats(self):
        index = load_index()
        papers = index["papers"]
        chunks = index["chunks"]
        return build_dashboard_stats(papers, chunks)

    def graph_stats(self):
        papers = get_papers()
        return graph_summary(papers)

    def graph_figure(self):
        papers = get_papers()
        return create_interactive_graph(papers)
