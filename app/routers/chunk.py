from fastapi import APIRouter, Depends

import app.loader
from app.database import crud, models, schemas
from app.loader.base import BaseLoader

router = APIRouter(prefix="/chunk", tags=["chunk"])


@router.post("/", response_model=schemas.ChunkOut)
async def create_chunk(chunk_create: schemas.ChunkCreate, db=Depends(models.get_db)):
    document = crud.get_document(db, chunk_create.document_id)
    if not document:
        raise ValueError("Document not found")

    if crud.get_chunks_by_document(db, document.id):
        raise ValueError("Chunks already exist for this document")

    # 根据 ChunkCreate 的 loader 字段，从 app.loader 中加载对应的 loader
    # TODO: 处理 loader 不存在的情况
    loader_class = getattr(app.loader, chunk_create.loader)
    if not loader_class:
        raise ValueError("Loader not found")

    loader: BaseLoader = loader_class()
    chunks = loader.load(document.raw_content, **chunk_create.args)

    return schemas.ChunkOut(
        document_id=chunk_create.document_id,
        loader=chunk_create.loader,
        args=chunk_create.args,
        size=await crud.create_chunks(db, chunks, document.id),
    )
