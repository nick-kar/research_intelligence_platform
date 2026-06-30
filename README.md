# Research Intelligence Platform

<p align="center">
  <img src="assets/banner.png" width="100%">
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-green)
![BM25](https://img.shields.io/badge/BM25-Hybrid_Retrieval-orange)
![RAG](https://img.shields.io/badge/RAG-LLM-purple)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-blueviolet)
![NetworkX](https://img.shields.io/badge/NetworkX-Knowledge_Graph-success)

</p>

---

## Overview

Research Intelligence Platform is an AI-powered scientific literature analysis system that enables researchers to explore large collections of academic papers through semantic retrieval and Retrieval-Augmented Generation (RAG).

The platform combines hybrid information retrieval (BM25 + FAISS), LLM reasoning, and knowledge graph visualization into a single interactive Streamlit application.

---

## Features

- Hybrid Retrieval (BM25 + FAISS)
- Grounded Question Answering
- Literature Review Generation
- Research Topic Comparison
- Research Gap Analysis
- Paper Inventory
- Interactive Knowledge Graph
- Retrieval Evaluation
- Dashboard Analytics

---

# Demo

## Dashboard

![](assets/screenshots/dashboard.png)

---

## Research Question Answering

![](assets/screenshots/ask-question.png)

---

## Literature Review Generation

![](assets/screenshots/literature-review.png)

---

## Research Topic Comparison

![](assets/screenshots/compare-topics.png)

---

## Research Gap Analysis

![](assets/screenshots/research-gap.png)

---

## Knowledge Graph

![](assets/screenshots/knowledge-graph.png)

---

## Retrieval Evaluation

![](assets/screenshots/evaluate-retrieval.png)

---

# System Architecture

<p align="center">
<img src="assets/architecture.png" width="100%">
</p>

The platform follows a five-stage pipeline:

1. PDF Ingestion
2. Hybrid Index Construction
3. Hybrid Retrieval
4. Retrieval-Augmented Generation
5. Interactive Visualization

---

## Technology Stack

| Category | Technology |
|-----------|------------|
| Programming | Python |
| Web Framework | Streamlit |
| Dense Retrieval | FAISS |
| Sparse Retrieval | BM25 |
| Embeddings | Sentence Transformers |
| Knowledge Graph | NetworkX |
| Visualization | Plotly |
| Data Processing | Pandas |

---

## Project Structure

```text
research-intelligence-platform
│
├── app/
├── assets/
│   ├── banner.png
│   ├── architecture.png
│   └── screenshots/
├── data/
│   ├── raw_papers/
│   └── index/
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/nick-kar/research_intelligence_platform.git
cd research_intelligence_platform
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Build the Search Index

Place PDF papers inside

```text
data/raw_papers/
```

Then run

```bash
python -m app.ingest
```

---

## Launch the Application

```bash
streamlit run app/main.py
```

---

## Current Capabilities

| Module | Status |
|----------|:------:|
| Dashboard | ✅ |
| Hybrid Retrieval | ✅ |
| Question Answering | ✅ |
| Literature Review | ✅ |
| Topic Comparison | ✅ |
| Research Gap Analysis | ✅ |
| Knowledge Graph | ✅ |
| Retrieval Evaluation | ✅ |

---

## Roadmap

- Cross-Encoder Reranking
- Citation Network Visualization
- Multi-document Summarization
- PDF Annotation
- arXiv Integration
- PubMed Integration
- CrossRef Integration
- Docker Support
- Multi-user Authentication

---

## Motivation

This project demonstrates practical applications of:

- Information Retrieval
- Scientific Document Intelligence
- Retrieval-Augmented Generation (RAG)
- Knowledge Graphs
- Natural Language Processing
- Interactive AI Systems

---

## License

MIT License

---

## Support

If you found this repository useful, consider giving it a ⭐.