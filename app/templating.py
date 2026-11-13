"""Configuração do Jinja2 (páginas HTML) e filtros de formatação."""
from datetime import datetime
from pathlib import Path

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


def moeda(valor: float | None) -> str:
    """Formata em Real: 1299.9 -> 'R$ 1.299,90'; None -> '-'."""
    if valor is None:
        return "-"
    texto = f"{valor:,.2f}"  # formato americano: 1,299.90
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def data_hora(valor: datetime) -> str:
    return valor.strftime("%d/%m/%Y %H:%M")


templates.env.filters["moeda"] = moeda
templates.env.filters["data_hora"] = data_hora
