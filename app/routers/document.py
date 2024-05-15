from fastapi import APIRouter, Depends

from app.database import crud, schemas
from app.database.models import get_db

router = APIRouter(prefix="/document", tags=["document"])


@router.get("/", response_model=list[schemas.Document])
async def read_documents(page: int = 0, size: int = 100, db=Depends(get_db)):
    return crud.get_documents(db, page * size, size)


@router.get("/{document_id}", response_model=schemas.Document)
async def read_document(document_id: str, db=Depends(get_db)):
    return crud.get_document(db, document_id)


@router.post("/", response_model=schemas.Document)
async def create_document(document: schemas.DocumentCreate, db=Depends(get_db)):
    return crud.create_document(db, document)
