from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class NameSpaceBase(BaseModel):
    name: str
    description: Optional[str] = None


class NameSpaceCreate(NameSpaceBase):
    pass


class NameSpace(NameSpaceBase):
    id: UUID4


class DocumentBase(BaseModel):
    title: str
    author: Optional[str] = None
    date: Optional[datetime] = None
    type: Optional[str] = None
    tags: Optional[list[str]] = None
    raw_content: str


class DocumentCreate(DocumentBase):
    namespace_id: str


class Document(DocumentBase):
    id: UUID4
    namespace_id: UUID4


class ChunkBase(BaseModel):
    content: str


class Chunk(ChunkBase):
    document_id: UUID4
    embedding: list[float]


class ChunkCreate(ChunkBase):
    document_id: str
