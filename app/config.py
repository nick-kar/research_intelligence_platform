from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_PAPERS_DIR = BASE_DIR / "data" / "raw_papers"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"

INDEX_FILE = VECTOR_STORE_DIR / "research_index.pkl"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
TOP_K = 6
SVD_COMPONENTS = 128
