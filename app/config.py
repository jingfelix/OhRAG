from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
    ollama_host: str = "http://localhost:11434"
    ollama_embed_model: str = "nomic-embed-text"
    dimension: int = 768  # defualt dimension of nomic-embed-text is 768
    sqlalchemy_database_uri: str = "postgresql://ohrag:ohrag@localhost:25432/ohrag"
    default_chunk_size: int = 8192

    class Config:
        env_file = ".env"


settings = get_settings()
