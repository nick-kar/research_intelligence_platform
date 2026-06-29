def build_literature_review(topic: str, results):
    if not results:
        return "No relevant literature found."

    background = []
    methods = []
    limitations = []
    future_work = []

    for result in results:
        text = result["text"]
        lower = text.lower()
        citation = f"[{result['source']}, p. {result['page']}]"

        item = f"- {text[:450]}... {citation}"

        if any(word in lower for word in ["limitation", "challenge", "constraint", "drawback"]):
            limitations.append(item)
        elif any(word in lower for word in ["future", "further", "improve", "recommend"]):
            future_work.append(item)
        elif any(word in lower for word in ["method", "simulation", "model", "algorithm", "approach"]):
            methods.append(item)
        else:
            background.append(item)

    review = f"# Literature Review Draft: {topic}\n\n"

    review += "## Background\n"
    review += "\n".join(background[:4]) if background else "No explicit background passages retrieved."
    review += "\n\n## Methods and Technical Approaches\n"
    review += "\n".join(methods[:4]) if methods else "No explicit methodology passages retrieved."
    review += "\n\n## Limitations and Challenges\n"
    review += "\n".join(limitations[:4]) if limitations else "No explicit limitation passages retrieved."
    review += "\n\n## Future Research Directions\n"
    review += "\n".join(future_work[:4]) if future_work else "No explicit future-work passages retrieved."

    return review
