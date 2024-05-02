from sqlalchemy.orm import Session

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
def create_chunks(db: Session, chunks: list[schemas.ChunkBase]) -> int:
    # TODO: Implement this function
    return len(chunks)
