from app.database.schemas import ChunkBase
from app.loader.base import BaseLoader

from .spliters import simple_splitter


class DefaultLoader(BaseLoader):
    def load(self, raw_content: str) -> list[ChunkBase]:
        chunks = []

        for chunk in simple_splitter(raw_content, self.chunk_size):
            chunks.append(ChunkBase(content=chunk))

        return chunks
