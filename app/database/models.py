import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, mapped_column, sessionmaker

_Base = declarative_base()
from app.config import settings

engine = create_engine(
    settings.sqlalchemy_database_uri,
    pool_recycle=3600,
    # connect_args={"check_same_thread": False},  # SQLite specific
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create DB
def init_db():
    session = SessionLocal()
    result = session.execute(text("SELECT 1 FROM pg_database WHERE datname = 'ohrag'"))
    if not result.scalar():
        session.execute(text("CREATE DATABASE ohrag"))

    # Create Extension
    session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    session.commit()

    _Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(_Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


class NameSpace(Base):
    __tablename__ = "namespace"

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)


class Document(Base):
    __tablename__ = "document"

    namespace_id = Column(Integer, ForeignKey("namespace.id"), nullable=False)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.datetime.now)
    type = Column(String(255), nullable=True)
    tags = Column(ARRAY(String), nullable=True)
    raw_content = Column(Text, nullable=False)


class Chunk(Base):
    __tablename__ = "chunk"

    document_id = Column(Integer, ForeignKey("document.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = mapped_column(Vector(settings.dimension))
