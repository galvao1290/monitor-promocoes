"""UC05 - Consultar Promoções (página inicial)."""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import listar_promocoes
from app.templating import templates

router = APIRouter(tags=["Promoções"])


@router.get("/")
def promocoes(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request, "promocoes.html", {"promocoes": listar_promocoes(db)}
    )
