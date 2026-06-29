import re
from collections import Counter


def extract_title(text: str) -> str:
    candidates = [line.strip() for line in text.split(".") if 30 <= len(line.strip()) <= 160]
    if candidates:
        return candidates[0]
    return "Unknown Title"


def extract_keywords(text: str, top_n: int = 12):
    words = re.findall(r"\b[a-zA-Z]{5,}\b", text.lower())

    stop_words = {
        "there", "their", "which", "using", "based", "these", "those",
        "paper", "study", "studies", "results", "method", "methods",
        "model", "models", "analysis", "research", "figure", "table",
        "different", "proposed", "however", "within", "between"
    }

    filtered = [word for word in words if word not in stop_words]
    counts = Counter(filtered)

    return [word for word, _ in counts.most_common(top_n)]


def extract_metadata(filename: str, full_text: str, num_pages: int):
    return {
        "filename": filename,
        "title": extract_title(full_text[:4000]),
        "keywords": extract_keywords(full_text),
        "num_pages": num_pages,
    }
