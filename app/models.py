"""Entidades do sistema: Loja, Categoria, Produto e HistoricoPreco."""
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Loja(Base):
    __tablename__ = "loja"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)
    site: Mapped[str | None] = mapped_column(String(255))

    produtos: Mapped[list["Produto"]] = relationship(back_populates="loja")


class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)
    descricao: Mapped[str | None] = mapped_column(String(255))

    produtos: Mapped[list["Produto"]] = relationship(back_populates="categoria")


class Produto(Base):
    __tablename__ = "produto"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(150))
    url: Mapped[str | None] = mapped_column(String(500))
    preco_alvo: Mapped[float] = mapped_column(Float)
    loja_id: Mapped[int] = mapped_column(ForeignKey("loja.id"))
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria.id"))
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    loja: Mapped[Loja] = relationship(back_populates="produtos")
    categoria: Mapped[Categoria] = relationship(back_populates="produtos")
    historico: Mapped[list["HistoricoPreco"]] = relationship(
        back_populates="produto",
        cascade="all, delete-orphan",
        order_by="(HistoricoPreco.data_registro.desc(), HistoricoPreco.id.desc())",
    )


class HistoricoPreco(Base):
    __tablename__ = "historico_preco"

    id: Mapped[int] = mapped_column(primary_key=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produto.id"))
    preco: Mapped[float] = mapped_column(Float)
    data_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    produto: Mapped[Produto] = relationship(back_populates="historico")
