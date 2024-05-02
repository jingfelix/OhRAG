from app.config import settings
from app.database.schemas import ChunkBase


class BaseLoader(object):
    # load config here
    chunk_size: int

    def __init__(self, chunk_size: int = settings.default_chunk_size) -> None:
        self.chunk_size = chunk_size

    def load(self, raw_content: str, **kwargs) -> list[ChunkBase]:
        pass
