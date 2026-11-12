"""UC02 - Gerenciar Categorias."""
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Categoria
from app.templating import templates

router = APIRouter(prefix="/categorias", tags=["Categorias"])

MSG_NOME = "O nome é obrigatório."
MSG_DUPLICADO = "Já existe um registro com esse nome."
MSG_VINCULADO = "Não é possível excluir: existem produtos vinculados."


def _pagina(request: Request, db: Session, editando: Categoria | None = None,
            erro: str | None = None, status: int = 200):
    categorias = db.query(Categoria).order_by(Categoria.nome).all()
    return templates.TemplateResponse(
        request, "categorias.html",
        {"categorias": categorias, "editando": editando, "erro": erro},
        status_code=status,
    )


def _buscar(db: Session, categoria_id: int) -> Categoria:
    categoria = db.get(Categoria, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return categoria


def _salvar(request: Request, db: Session, categoria: Categoria, nome: str, descricao: str):
    nome = nome.strip()
    if not nome:
        db.rollback()
        return _pagina(request, db, categoria if categoria.id else None, MSG_NOME, 400)
    categoria.nome = nome
    categoria.descricao = descricao.strip() or None
    db.add(categoria)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return _pagina(request, db, categoria if categoria.id else None, MSG_DUPLICADO, 400)
    return RedirectResponse("/categorias", status_code=303)


@router.get("")
def listar(request: Request, db: Session = Depends(get_db)):
    return _pagina(request, db)


@router.post("")
def criar(request: Request, nome: str = Form(""), descricao: str = Form(""),
          db: Session = Depends(get_db)):
    return _salvar(request, db, Categoria(), nome, descricao)


@router.get("/{categoria_id}/editar")
def editar_form(categoria_id: int, request: Request, db: Session = Depends(get_db)):
    return _pagina(request, db, editando=_buscar(db, categoria_id))


@router.post("/{categoria_id}/editar")
def editar(categoria_id: int, request: Request, nome: str = Form(""), descricao: str = Form(""),
           db: Session = Depends(get_db)):
    return _salvar(request, db, _buscar(db, categoria_id), nome, descricao)


@router.post("/{categoria_id}/excluir")
def excluir(categoria_id: int, request: Request, db: Session = Depends(get_db)):
    categoria = _buscar(db, categoria_id)
    if categoria.produtos:
        return _pagina(request, db, erro=MSG_VINCULADO, status=400)
    db.delete(categoria)
    db.commit()
    return RedirectResponse("/categorias", status_code=303)
