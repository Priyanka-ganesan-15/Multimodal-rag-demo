from app.core.config import settings
from app.services.supabase_client import get_supabase


def download_bytes(storage_path: str) -> bytes:
    """
    Downloads an object from Supabase Storage and returns raw bytes.
    storage_path should be the exact path stored in DB (e.g. collection/fileId/demo.pdf)
    """
    supabase = get_supabase()
    data = supabase.storage.from_(settings.SUPABASE_BUCKET).download(storage_path)
    # supabase-py returns raw bytes for download()
    return data
