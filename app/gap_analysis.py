from collections import Counter
import re


def analyze_research_gaps(topic: str, results):
    if not results:
        return "No relevant evidence found for gap analysis."

    combined_text = " ".join([r["text"] for r in results]).lower()

    terms = re.findall(r"\b[a-zA-Z]{6,}\b", combined_text)

    stop_words = {
        "method", "methods", "results", "system", "systems", "analysis",
        "different", "using", "between", "through", "because", "however",
        "research", "paper", "study", "studies"
    }

    counts = Counter([term for term in terms if term not in stop_words])
    top_terms = [term for term, _ in counts.most_common(15)]

    gap_text = f"# Research Gap Analysis: {topic}\n\n"

    gap_text += "## Frequently Retrieved Concepts\n"
    gap_text += ", ".join(top_terms) + "\n\n"

    gap_text += "## Potential Research Gaps\n"
    gap_text += "- Experimental validation may be limited if retrieved evidence focuses mainly on simulation studies.\n"
    gap_text += "- Dataset diversity may be limited if studies rely on narrow tissue models, small samples, or simplified assumptions.\n"
    gap_text += "- Real-time deployment may require stronger validation, robustness analysis, and computational efficiency.\n"
    gap_text += "- Explainability may be underdeveloped if machine learning models are used without interpretation methods.\n"
    gap_text += "- Clinical translation may require additional uncertainty quantification and reproducibility analysis.\n\n"

    gap_text += "## Suggested Future Directions\n"
    gap_text += "- Combine physics-based simulation with machine learning.\n"
    gap_text += "- Add explainable AI methods for model interpretation.\n"
    gap_text += "- Evaluate robustness across heterogeneous datasets.\n"
    gap_text += "- Develop reproducible open-source pipelines.\n"

    return gap_text
