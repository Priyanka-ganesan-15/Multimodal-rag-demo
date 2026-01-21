def chunk_text(text: str, max_chars: int = 1600, overlap: int = 200) -> list[str]:
    """
    Fast char-based chunker for MVP.
    Keeps overlap to preserve context across chunks.
    """
    text = (text or "").strip()
    if not text:
        return []

    chunks: list[str] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= n:
            break

        start = max(0, end - overlap)

    return chunks
