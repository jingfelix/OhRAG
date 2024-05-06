from whatthepatch import parse_patch

from app.database.schemas import ChunkBase
from app.loader.base import BaseLoader

from .spliters import simple_splitter


class PatchLoader(BaseLoader):
    def load(self, raw_content: str, **kwargs) -> list[ChunkBase]:
        diffes = parse_patch(raw_content)

        chunks: list[ChunkBase] = []
        for diff in diffes:
            if len(diff.text) <= self.chunk_size:
                chunks.append(
                    ChunkBase(
                        content=diff.text,
                    )
                )
            else:
                for chunk in simple_splitter(diff.text, self.chunk_size):
                    chunks.append(
                        ChunkBase(
                            content=chunk,
                        )
                    )

        return chunks
