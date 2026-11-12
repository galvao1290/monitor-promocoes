"""Regras de negócio: interpretação de preços e detecção de promoções."""
from dataclasses import dataclass

from sqlalchemy.orm import Session, selectinload

from app.models import Produto

MSG_PRECO_INVALIDO = "Informe um preço válido maior que zero."


def parse_preco(texto: str) -> float:
    """Converte '1.299,90', '19,90', 'R$ 10' ou '25.5' em float (2 casas)."""
    limpo = (texto or "").replace("R$", "").strip().replace(" ", "")
    if "," in limpo:
        limpo = limpo.replace(".", "").replace(",", ".")
    try:
        valor = round(float(limpo), 2)
    except ValueError:
        raise ValueError(MSG_PRECO_INVALIDO) from None
    if valor <= 0:
        raise ValueError(MSG_PRECO_INVALIDO)
    return valor


def preco_atual(produto: Produto) -> float | None:
    """Último preço registrado (o histórico já vem do mais recente ao mais antigo)."""
    return produto.historico[0].preco if produto.historico else None


def menor_preco(produto: Produto) -> float | None:
    return min((h.preco for h in produto.historico), default=None)


def em_promocao(produto: Produto) -> bool:
    atual = preco_atual(produto)
    return atual is not None and atual <= produto.preco_alvo


@dataclass
class Promocao:
    produto: Produto
    preco_atual: float
    economia: float
    menor_preco: float


def listar_promocoes(db: Session) -> list[Promocao]:
    """Produtos cujo preço atual está igual ou abaixo do preço-alvo, maior economia primeiro."""
    produtos = (
        db.query(Produto)
        .options(selectinload(Produto.historico), selectinload(Produto.loja))
        .all()
    )
    promocoes = [
        Promocao(
            produto=p,
            preco_atual=preco_atual(p),
            economia=round(p.preco_alvo - preco_atual(p), 2),
            menor_preco=menor_preco(p),
        )
        for p in produtos
        if em_promocao(p)
    ]
    return sorted(promocoes, key=lambda x: x.economia, reverse=True)
