import streamlit as st
import pandas as pd

from app.research_agent import ResearchAgent

st.set_page_config(
    page_title="Research Intelligence Platform",
    page_icon="??",
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
        "Dashboard",
        "Ask Research Question",
        "Generate Literature Review",
        "Compare Topics",
        "Research Gap Analysis",
        "Paper Inventory",
        "Knowledge Graph Summary",
        "Evaluate Retrieval",
    ],
)

st.sidebar.markdown("---")
st.sidebar.write("Add PDFs to:")
st.sidebar.code("data/raw_papers/")
st.sidebar.write("Then build index:")
st.sidebar.code("python -m app.ingest")

try:
    if mode == "Dashboard":
        stats = agent.dashboard_stats()

        c1, c2, c3 = st.columns(3)
        c1.metric("Papers", stats["num_papers"])
        c2.metric("Indexed Chunks", stats["num_chunks"])
        c3.metric("Total Pages", stats["total_pages"])

        st.subheader("Top Keywords")
        st.dataframe(pd.DataFrame(stats["top_keywords"], columns=["Keyword", "Frequency"]))

    elif mode == "Ask Research Question":
        question = st.text_input("Research question")

        if st.button("Run") and question:
            answer, sources = agent.answer_question(question)
            st.markdown(answer)
            st.subheader("Sources")
            st.dataframe(pd.DataFrame(sources, columns=["Source", "Page"]))

    elif mode == "Generate Literature Review":
        topic = st.text_input("Literature review topic")

        if st.button("Generate") and topic:
            review, sources = agent.literature_review(topic)
            st.markdown(review)
            st.subheader("Sources")
            st.dataframe(pd.DataFrame(sources, columns=["Source", "Page"]))

    elif mode == "Compare Topics":
        topic_a = st.text_input("Topic A")
        topic_b = st.text_input("Topic B")

        if st.button("Compare") and topic_a and topic_b:
            comparison, sources = agent.compare_topics(topic_a, topic_b)
            st.markdown(comparison)
            st.subheader("Sources")
            st.dataframe(pd.DataFrame(sources, columns=["Source", "Page"]))

    elif mode == "Research Gap Analysis":
        topic = st.text_input("Topic")

        if st.button("Analyze") and topic:
            gaps, sources = agent.research_gap_analysis(topic)
            st.markdown(gaps)
            st.subheader("Sources")
            st.dataframe(pd.DataFrame(sources, columns=["Source", "Page"]))

    elif mode == "Paper Inventory":
        st.markdown(agent.paper_inventory())

    elif mode == "Knowledge Graph Summary":
        stats = agent.graph_stats()

        c1, c2, c3 = st.columns(3)
        c1.metric("Graph Nodes", stats["nodes"])
        c2.metric("Graph Edges", stats["edges"])
        c3.metric("Indexed Papers", stats["papers"])

        st.subheader("Interactive Paper–Keyword Graph")
        fig = agent.graph_figure()
        st.plotly_chart(fig, use_container_width=True)

    elif mode == "Evaluate Retrieval":
        from app.evaluation import evaluate_query

        query = st.text_input("Evaluation query")
        relevant_sources_text = st.text_area(
            "Relevant source filenames, one per line",
            help="Example: paper1.pdf"
        )

        if st.button("Evaluate") and query:
            relevant_sources = [
                line.strip()
                for line in relevant_sources_text.splitlines()
                if line.strip()
            ]

            metrics = evaluate_query(query, relevant_sources, k=5)

            st.subheader("Retrieval Metrics")
            st.json(metrics)

except FileNotFoundError:
    st.warning("No index found. Add PDF files to data/raw_papers/ and run: python -m app.ingest")
except Exception as error:
    st.error(f"Error: {error}")
