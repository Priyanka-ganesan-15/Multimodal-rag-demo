import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.db.models import File, Collection
from app.services.supabase_client import get_supabase

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/init-upload")
def init_upload(
    collection_id: str,
    filename: str,
    mime_type: str | None = None,
    db: Session = Depends(get_db),
):
    # 1) Validate collection exists
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    # 2) Create file record (status=uploaded)
    file_id = str(uuid.uuid4())
    storage_path = f"{collection_id}/{file_id}/{filename}"

    file_row = File(
        id=file_id,
        collection_id=collection_id,
        filename=filename,
        storage_path=storage_path,
        mime_type=mime_type,
        status="uploaded",
    )
    db.add(file_row)
    db.commit()
    db.refresh(file_row)

    # 3) Create a signed upload URL (valid for 10 minutes)
    supabase = get_supabase()

    signed = supabase.storage.from_(settings.SUPABASE_BUCKET).create_signed_upload_url(
        path=storage_path
    )

    # Supabase python client usually returns dict with signedUrl/token
    if not signed or "signedUrl" not in signed:
        raise HTTPException(status_code=500, detail=f"Failed to create signed upload URL: {signed}")

    return {
        "file": {
            "id": str(file_row.id),
            "collection_id": str(file_row.collection_id),
            "filename": file_row.filename,
            "storage_path": file_row.storage_path,
            "status": file_row.status,
        },
        "upload": {
            "signedUrl": signed["signedUrl"],
            "token": signed.get("token"),
            "bucket": settings.SUPABASE_BUCKET,
        },
    }
