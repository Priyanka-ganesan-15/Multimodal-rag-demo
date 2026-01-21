from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Collection

router = APIRouter(prefix="/collections", tags=["collections"])


@router.post("")
def create_collection(name: str, db: Session = Depends(get_db)):
    collection = Collection(name=name)
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection


@router.get("")
def list_collections(db: Session = Depends(get_db)):
    return db.query(Collection).order_by(Collection.created_at.desc()).all()
