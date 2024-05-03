from fastapi import APIRouter, Depends

from app.database import crud, models, schemas

router = APIRouter(prefix="/query", tags=["query"])


@router.get("/", response_model=list[schemas.ChunkQuery])
async def get_chunks_by_query(query: schemas.ChunkQuery, db=Depends(models.get_db)):
    document = crud.get_document(db, query.document_id)
    if not document:
        raise ValueError("Document not found")

    if not query.content:
        raise ValueError("Query content is empty")

    chunks = await crud.get_chunks_by_query(db, query)
    return [
        schemas.ChunkQuery(
            content=chunk.content,
            document_id=str(chunk.document_id),
        )
        for chunk in chunks
    ]
