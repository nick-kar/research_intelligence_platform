from app.utils import clean_text, chunk_text


def test_clean_text_removes_extra_spaces():
    text = "Hello\n\n     world"
    assert clean_text(text) == "Hello world"


def test_chunk_text_creates_multiple_chunks():
    text = "a" * 3000
    chunks = chunk_text(text, chunk_size=1000, overlap=100)
    assert len(chunks) > 1


def test_chunk_text_returns_strings():
    text = "research intelligence platform " * 200
    chunks = chunk_text(text, chunk_size=500, overlap=100)
    assert all(isinstance(chunk, str) for chunk in chunks)