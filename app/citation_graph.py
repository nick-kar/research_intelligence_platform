import networkx as nx
import plotly.graph_objects as go


def build_keyword_graph(papers):
    graph = nx.Graph()

    for paper in papers:
        paper_node = paper["filename"]
        graph.add_node(paper_node, type="paper")

        for keyword in paper.get("keywords", [])[:8]:
            graph.add_node(keyword, type="keyword")
            graph.add_edge(paper_node, keyword)

    return graph


def graph_summary(papers):
    graph = build_keyword_graph(papers)

    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "papers": len(papers),
    }


def create_interactive_graph(papers):
    graph = build_keyword_graph(papers)
    pos = nx.spring_layout(graph, seed=42)

    edge_x = []
    edge_y = []

    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x = []
    node_y = []
    node_text = []
    node_size = []

    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        node_size.append(18 if graph.nodes[node].get("type") == "paper" else 10)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5),
        hoverinfo="none",
        mode="lines",
    )

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        hoverinfo="text",
        marker=dict(size=node_size),
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Paper–Keyword Knowledge Graph",
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        height=700,
    )

    return fig