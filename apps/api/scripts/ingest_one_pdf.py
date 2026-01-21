import sys
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import File, Chunk
from app.services.storage import download_bytes
from app.services.pdf_extract import extract_pdf_pages
from app.services.chunking import chunk_text


def ingest_file(db: Session, file_id: str) -> None:
    file_row = db.query(File).filter(File.id == file_id).first()
    if not file_row:
        raise RuntimeError("File not found in DB")

    # mark indexing
    file_row.status = "indexing"
    db.commit()

    data = download_bytes(file_row.storage_path)
    pages = extract_pdf_pages(data)

    # clear old chunks
    db.query(Chunk).filter(Chunk.file_id == file_row.id).delete()
    db.commit()

    chunk_index = 0
    total = 0

    for page_num, page_text in pages:
        for c in chunk_text(page_text):
            db.add(
                Chunk(
                    file_id=file_row.id,
                    collection_id=file_row.collection_id,
                    chunk_index=chunk_index,
                    content=c,
                    source_type="pdf_text",
                    page=page_num,
                    meta={"filename": file_row.filename},

                )
            )
            chunk_index += 1
            total += 1

    file_row.status = "indexed"
    db.commit()

    print(f"Ingested file_id={file_id} pages={len(pages)} chunks={total} status={file_row.status}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/ingest_one_pdf.py <file_id>")
        sys.exit(1)

    fid = sys.argv[1]
    db = SessionLocal()
    try:
        ingest_file(db, fid)
    finally:
        db.close()
