import fitz  # PyMuPDF


def extract_pdf_pages(pdf_bytes: bytes) -> list[tuple[int, str]]:
    """
    Returns a list of (page_number, text) tuples.
    Page numbers are 1-based.
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages: list[tuple[int, str]] = []

    for i in range(len(doc)):
        page = doc.load_page(i)
        text = page.get_text("text") or ""
        text = text.strip()
        if text:
            pages.append((i + 1, text))

    return pages
