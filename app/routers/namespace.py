from fastapi import APIRouter, Depends

from app.database import crud, schemas
from app.database.models import get_db

router = APIRouter(prefix="/namespace", tags=["namespace"])


@router.get("/", response_model=list[schemas.NameSpace])
async def read_namespaces(page: int = 0, size: int = 100, db=Depends(get_db)):
    return crud.get_namespaces(db, page * size, size)


@router.get("/{namespace_name}", response_model=schemas.NameSpace)
async def read_namespace(namespace_name: str, db=Depends(get_db)):
    return crud.get_namespace_by_name(db, namespace_name)


@router.post("/", response_model=schemas.NameSpace)
async def create_namespace(namespace: schemas.NameSpaceCreate, db=Depends(get_db)):
    return crud.create_namespace(db, namespace)
