import streamlit as st
import pandas as pd

from app.research_agent import ResearchAgent
from app.hybrid_retriever import hybrid_search

st.set_page_config(
    page_title="Research Intelligence Platform",
    page_icon="🧠",
    layout="wide",
)

agent = ResearchAgent()

st.title("Research Intelligence Platform")
st.write(
    "A scientific AI platform for querying, comparing, reviewing, and extracting insights from research papers."
)

st.sidebar.title("Tools")
mode = st.sidebar.radio(
    "Select tool",
    [
        "📊 Dashboard",
        "🔍 Ask Research Question",
        "📚 Generate Literature Review",
        "⚖️ Compare Topics",
        "🧠 Research Gap Analysis",
        "📄 Paper Inventory",
        "🕸️ Knowledge Graph Summary",
        "📈 Evaluate Retrieval",
    ],
)

st.sidebar.markdown("---")
st.sidebar.write("Add PDFs to:")
st.sidebar.code("data/raw_papers/")
st.sidebar.write("Then build indexes:")
st.sidebar.code("python -m app.ingest")
st.sidebar.code("python -m app.semantic_index")


def show_sources(sources):
    st.subheader("Sources")
    st.dataframe(pd.DataFrame(sources, columns=["Source", "Page"]), use_container_width=True)


try:
    if mode == "📊 Dashboard":
        stats = agent.dashboard_stats()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Papers", stats["num_papers"])
        c2.metric("Indexed Chunks", stats["num_chunks"])
        c3.metric("Total Pages", stats["total_pages"])
        c4.metric("Avg. Chunks / Paper", round(stats["num_chunks"] / stats["num_papers"], 1))

        st.subheader("Top Keywords")
        st.dataframe(
            pd.DataFrame(stats["top_keywords"], columns=["Keyword", "Frequency"]),
            use_container_width=True,
        )

    elif mode == "🔍 Ask Research Question":
        question = st.text_input(
            "Research question",
            placeholder="Example: How does dielectric property variation affect microwave ablation efficiency?",
        )

        if st.button("Run") and question:
            answer, sources = agent.answer_question(question)
            results = hybrid_search(question, top_k=8)

            st.markdown("# Grounded Research Answer")
            st.markdown(f"### Question\n{question}")

            for i, r in enumerate(results, start=1):
                with st.container(border=True):
                    st.subheader(f"Evidence {i}")

                    c1, c2, c3 = st.columns(3)
                    c1.metric("Score", f"{r.get('rerank_score', r.get('score', 0.0)):.3f}")
                    c2.metric("Page", r["page"])
                    c3.metric("Retriever", r.get("retriever", "hybrid"))

                    st.caption(r["source"])
                    st.write(r["text"])

            show_sources(sources)

    elif mode == "📚 Generate Literature Review":
        topic = st.text_input(
            "Literature review topic",
            placeholder="Example: Microwave Ablation",
        )

        if st.button("Generate") and topic:
            review, sources = agent.literature_review(topic)

            st.markdown(review)
            show_sources(sources)

    elif mode == "⚖️ Compare Topics":
        col1, col2 = st.columns(2)

        with col1:
            topic_a = st.text_input("Topic A", placeholder="Example: Microwave Ablation")

        with col2:
            topic_b = st.text_input("Topic B", placeholder="Example: Radiofrequency Ablation")

        if st.button("Compare") and topic_a and topic_b:
            comparison, sources = agent.compare_topics(topic_a, topic_b)

            st.markdown(comparison)
            show_sources(sources)

    elif mode == "🧠 Research Gap Analysis":
        topic = st.text_input(
            "Topic",
            placeholder="Example: Microwave Ablation",
        )

        if st.button("Analyze") and topic:
            gaps, sources = agent.research_gap_analysis(topic)

            st.markdown(gaps)
            show_sources(sources)

    elif mode == "📄 Paper Inventory":
        st.markdown(agent.paper_inventory())

    elif mode == "🕸️ Knowledge Graph Summary":
        stats = agent.graph_stats()

        c1, c2, c3 = st.columns(3)
        c1.metric("Graph Nodes", stats["nodes"])
        c2.metric("Graph Edges", stats["edges"])
        c3.metric("Indexed Papers", stats["papers"])

        st.subheader("Interactive Paper–Keyword Graph")
        fig = agent.graph_figure()
        st.plotly_chart(fig, use_container_width=True)

    elif mode == "📈 Evaluate Retrieval":
        from app.evaluation import evaluate_query

        query = st.text_input(
            "Evaluation query",
            placeholder="Example: microwave ablation limitations",
        )

        relevant_sources_text = st.text_area(
            "Relevant source filenames, one per line",
            help="Example: paper1.pdf",
        )

        if st.button("Evaluate") and query:
            relevant_sources = [
                line.strip()
                for line in relevant_sources_text.splitlines()
                if line.strip()
            ]

            metrics = evaluate_query(query, relevant_sources, k=5)

            st.subheader("Retrieval Metrics")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Precision@5", f"{metrics['precision_at_k']:.2f}")
            c2.metric("Recall@5", f"{metrics['recall_at_k']:.2f}")
            c3.metric("MRR", f"{metrics['mrr']:.2f}")
            c4.metric("nDCG@5", f"{metrics['ndcg_at_k']:.2f}")
            c5.metric("Latency", f"{metrics['latency_seconds']:.2f}s")

            st.subheader("Retrieved Sources")
            st.dataframe(
                pd.DataFrame(metrics["retrieved_sources"], columns=["Retrieved Source"]),
                use_container_width=True,
            )

except FileNotFoundError:
    st.warning(
        "No index found. Add PDF files to data/raw_papers/ and run: "
        "python -m app.ingest and python -m app.semantic_index"
    )
except Exception as error:
    st.error(f"Error: {error}")