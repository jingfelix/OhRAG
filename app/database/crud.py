from sqlalchemy.orm import Session

from app.database import models, schemas


def get_namespace(db: Session, namespace_id: int) -> models.NameSpace | None:
    return (
        db.query(models.NameSpace).filter(models.NameSpace.id == namespace_id).first()
    )


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
