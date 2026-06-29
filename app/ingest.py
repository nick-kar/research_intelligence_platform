import pickle
import fitz
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize

from app.config import (
    RAW_PAPERS_DIR,
    VECTOR_STORE_DIR,
    INDEX_FILE,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    SVD_COMPONENTS,
)
from app.utils import clean_text, chunk_text
from app.metadata import extract_metadata


def extract_pdf_pages(pdf_path):
    document = fitz.open(pdf_path)
    pages = []
    full_text = ""

    for page_number, page in enumerate(document, start=1):
        text = clean_text(page.get_text())
        full_text += " " + text

        if text:
            pages.append({
                "source": pdf_path.name,
                "page": page_number,
                "text": text,
            })

    metadata = extract_metadata(
        filename=pdf_path.name,
        full_text=full_text,
        num_pages=len(document),
    )

    return pages, metadata


def build_index():
    RAW_PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(RAW_PAPERS_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in data/raw_papers.")
        return

    chunks = []
    papers = []

    for pdf_path in pdf_files:
        pages, metadata = extract_pdf_pages(pdf_path)
        papers.append(metadata)

        for page in pages:
            page_chunks = chunk_text(page["text"], CHUNK_SIZE, CHUNK_OVERLAP)

            for chunk_id, chunk in enumerate(page_chunks):
                chunks.append({
                    "text": chunk,
                    "source": page["source"],
                    "page": page["page"],
                    "chunk_id": chunk_id,
                })

    documents = [chunk["text"] for chunk in chunks]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=30000,
        ngram_range=(1, 2),
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    n_components = min(
        SVD_COMPONENTS,
        tfidf_matrix.shape[1] - 1,
        tfidf_matrix.shape[0] - 1,
    )

    if n_components < 2:
        raise ValueError("Not enough text data to build vector index. Add more PDF content.")

    svd = TruncatedSVD(n_components=n_components, random_state=42)
    dense_vectors = svd.fit_transform(tfidf_matrix)
    dense_vectors = normalize(dense_vectors).astype("float32")

    faiss_index = faiss.IndexFlatIP(dense_vectors.shape[1])
    faiss_index.add(dense_vectors)

    index_data = {
        "vectorizer": vectorizer,
        "svd": svd,
        "faiss_index": faiss_index,
        "chunks": chunks,
        "papers": papers,
    }

    with open(INDEX_FILE, "wb") as file:
        pickle.dump(index_data, file)

    print(f"Indexed {len(chunks)} chunks from {len(pdf_files)} papers.")
    print(f"FAISS index dimension: {dense_vectors.shape[1]}")


if __name__ == "__main__":
    build_index()
