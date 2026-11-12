"""UC01 - Gerenciar Lojas."""
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Loja
from app.templating import templates

router = APIRouter(prefix="/lojas", tags=["Lojas"])

MSG_NOME = "O nome é obrigatório."
MSG_DUPLICADO = "Já existe um registro com esse nome."
MSG_VINCULADO = "Não é possível excluir: existem produtos vinculados."


def _pagina(request: Request, db: Session, editando: Loja | None = None,
            erro: str | None = None, status: int = 200):
    lojas = db.query(Loja).order_by(Loja.nome).all()
    return templates.TemplateResponse(
        request, "lojas.html",
        {"lojas": lojas, "editando": editando, "erro": erro},
        status_code=status,
    )


def _buscar(db: Session, loja_id: int) -> Loja:
    loja = db.get(Loja, loja_id)
    if loja is None:
        raise HTTPException(status_code=404, detail="Loja não encontrada.")
    return loja


def _salvar(request: Request, db: Session, loja: Loja, nome: str, site: str):
    nome = nome.strip()
    if not nome:
        db.rollback()
        return _pagina(request, db, loja if loja.id else None, MSG_NOME, 400)
    loja.nome = nome
    loja.site = site.strip() or None
    db.add(loja)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return _pagina(request, db, loja if loja.id else None, MSG_DUPLICADO, 400)
    return RedirectResponse("/lojas", status_code=303)


@router.get("")
def listar(request: Request, db: Session = Depends(get_db)):
    return _pagina(request, db)


@router.post("")
def criar(request: Request, nome: str = Form(""), site: str = Form(""),
          db: Session = Depends(get_db)):
    return _salvar(request, db, Loja(), nome, site)


@router.get("/{loja_id}/editar")
def editar_form(loja_id: int, request: Request, db: Session = Depends(get_db)):
    return _pagina(request, db, editando=_buscar(db, loja_id))


@router.post("/{loja_id}/editar")
def editar(loja_id: int, request: Request, nome: str = Form(""), site: str = Form(""),
           db: Session = Depends(get_db)):
    return _salvar(request, db, _buscar(db, loja_id), nome, site)


@router.post("/{loja_id}/excluir")
def excluir(loja_id: int, request: Request, db: Session = Depends(get_db)):
    loja = _buscar(db, loja_id)
    if loja.produtos:
        return _pagina(request, db, erro=MSG_VINCULADO, status=400)
    db.delete(loja)
    db.commit()
    return RedirectResponse("/lojas", status_code=303)
