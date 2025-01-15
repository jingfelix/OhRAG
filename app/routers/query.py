from fastapi import APIRouter, Depends

from app.database import crud, models, schemas

router = APIRouter(prefix="/query", tags=["query"])


@router.post("/", response_model=list[schemas.ChunkQuery])
async def get_chunks_by_query(
    query: schemas.ChunkBase,
    namespace_id: str = None,
    document_id: str = None,
    db=Depends(models.get_db),
):
    if namespace_id:
        namespace = crud.get_namespace(db, namespace_id)
        if not namespace:
            raise ValueError("Namespace not found")

    if document_id:
        document = crud.get_document(db, document_id)
        if not document:
            raise ValueError("Document not found")

    if not query.content:
        raise ValueError("Query content is empty")

    chunks = crud.get_chunks_by_query(db, query, namespace_id, document_id)
    return [
        schemas.ChunkQuery(
            content=chunk.content,
            document_id=str(chunk.document_id),
        )
        for chunk in chunks
    ]
