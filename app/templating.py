"""Configuração do Jinja2 (páginas HTML) e filtros de formatação."""
from pathlib import Path

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
