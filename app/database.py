"""Conexão com o banco SQLite e sessão do SQLAlchemy."""
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = "sqlite:///./monitor.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Iterator[Session]:
    """Abre uma sessão por requisição e fecha ao final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Cria as tabelas, caso ainda não existam."""
    from app import models  # noqa: F401  (registra os modelos no Base)

    Base.metadata.create_all(engine)
