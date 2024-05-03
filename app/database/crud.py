from ollama import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import models, schemas


# Universal function to get an item by its id
def get_item_by_id(db: Session, table: models.Base, _id: str) -> models.Base | None:
    return db.query(table).filter(table.id == _id).first()


# namespace CRUD functions
def get_namespace(db: Session, namespace_id: str) -> models.NameSpace | None:
    return get_item_by_id(db, models.NameSpace, namespace_id)


def get_namespace_by_name(db: Session, name: str) -> models.NameSpace | None:
    return db.query(models.NameSpace).filter(models.NameSpace.name == name).first()


def get_namespaces(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.NameSpace]:
    return db.query(models.NameSpace).offset(skip).limit(limit).all()


def create_namespace(
    db: Session, namespace: schemas.NameSpaceCreate
) -> models.NameSpace:
    if get_namespace_by_name(db, namespace.name):
        raise ValueError("Namespace already exists")

    db_namespace = models.NameSpace(
        name=namespace.name,
        description=namespace.description,
    )
    db.add(db_namespace)
    db.commit()
    db.refresh(db_namespace)

    return db_namespace


# document CRUD functions
def get_document(db: Session, document_id: str) -> models.Document | None:
    return get_item_by_id(db, models.Document, document_id)


def get_document_by_title(db: Session, title: str) -> models.Document | None:
    return db.query(models.Document).filter(models.Document.title == title).first()


def get_document_by_namespace(db: Session, namespace_id: str) -> list[models.Document]:
    return (
        db.query(models.Document)
        .filter(models.Document.namespace_id == namespace_id)
        .all()
    )


def get_documents(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.Document]:
    return db.query(models.Document).offset(skip).limit(limit).all()


def create_document(db: Session, document: schemas.DocumentCreate) -> models.Document:
    if get_document_by_title(db, document.title):
        raise ValueError("Document already exists")

    if not get_namespace(db, document.namespace_id):
        raise ValueError("Namespace does not exist")

    db_document = models.Document(
        namespace_id=document.namespace_id,
        title=document.title,
        author=document.author,
        date=document.date,
        type=document.type,
        tags=document.tags,
        raw_content=document.raw_content,
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return db_document


# chunk CRUD functions and task functions
async def create_chunks(
    db: Session, chunks: list[schemas.ChunkBase], document_id: str
) -> int:
    client = AsyncClient(host=settings.ollama_host)
    for chunk_base in chunks:
        res = await client.embeddings(
            model=settings.ollama_embed_model,
            prompt=chunk_base.content,
        )

        if not res.get("embedding", None):
            raise ValueError("Failed to get embedding")

        db_chunk = models.Chunk(
            document_id=document_id,
            content=chunk_base.content,
            embedding=res["embedding"],
        )

        db.add(db_chunk)
        db.flush()

    db.commit()

    return len(chunks)


def get_chunks_by_document(db: Session, document_id: str) -> list[models.Chunk]:
    return db.query(models.Chunk).filter(models.Chunk.document_id == document_id).all()


# Query functions
async def get_chunks_by_query(
    db: Session, query: schemas.ChunkQuery
) -> list[models.Chunk]:
    # 计算 Query 中的 content 的 embedding
    client = AsyncClient(host=settings.ollama_host)
    res = await client.embeddings(
        model=settings.ollama_embed_model,
        prompt=query.content,
    )
    if not res.get("embedding", None):
        raise ValueError("Failed to get embedding")

    # 当 document_id 不为空时，在对应 Document 的 Chunk 中搜索
    # 当 document_id 为空时，在所有 Chunk 中搜索

    # 使用 pgvector 的相似度函数
    return db.scalars(
        select(models.Chunk)
        .filter(
            models.Chunk.document_id == query.document_id if query.document_id else True
        )
        .order_by(models.Chunk.embedding.cosine_distance(res["embedding"]))
        .filter(
            models.Chunk.embedding.cosine_distance(res["embedding"]) > 0.5
        )  # TODO: 需要选择更好的过滤方案
        .limit(10)
    ).all()
