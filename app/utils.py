import re


def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int, overlap: int):
    chunks = []
    start = 0

    while start < len(text):
        chunk = text[start:start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def extract_possible_title(text: str) -> str:
    lines = [line.strip() for line in text.split(".") if len(line.strip()) > 20]
    return lines[0][:140] if lines else "Unknown Title"


def extract_keywords(text: str, top_n: int = 8):
    words = re.findall(r"\b[a-zA-Z]{5,}\b", text.lower())
    stop = {
        "there", "their", "which", "using", "based", "these", "those",
        "paper", "study", "results", "method", "methods", "model"
    }
    freq = {}
    for word in words:
        if word not in stop:
            freq[word] = freq.get(word, 0) + 1

    return [w for w, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_n]]
