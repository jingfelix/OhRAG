from typing import Optional

from pydantic import BaseModel


class NameSpaceBase(BaseModel):
    name: str
    description: Optional[str] = None


class NameSpaceCreate(NameSpaceBase):
    pass


class NameSpace(NameSpaceBase):
    pass


class DocumentBase(BaseModel):
    title: str
    author: Optional[str] = None
    date: Optional[str] = None
    type: Optional[str] = None
    tags: Optional[list[str]] = None
    raw_content: str


class DocumentCreate(DocumentBase):
    namespace_id: int
    pass


class ChunkBase(BaseModel):
    chunk_index: int
    content: str
    pass


class ChunkCreate(ChunkBase):
    document_id: int
    pass
