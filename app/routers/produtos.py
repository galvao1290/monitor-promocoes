"""UC03 - Gerenciar Produtos e UC04 - Registrar Preço."""
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Categoria, HistoricoPreco, Loja, Produto
from app.services import em_promocao, menor_preco, parse_preco, preco_atual
from app.templating import templates

router = APIRouter(tags=["Produtos"])

MSG_NOME = "O nome é obrigatório."
MSG_VINCULO = "Selecione uma loja e uma categoria."


def _buscar(db: Session, produto_id: int) -> Produto:
    produto = db.get(Produto, produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return produto


def _para_int(valor: str) -> int | None:
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def _formulario(request: Request, db: Session, produto: Produto | None,
                dados: dict | None = None, erro: str | None = None, status: int = 200):
    """Tela de cadastro/edição. `dados` guarda o que o usuário digitou em caso de erro."""
    if dados is None:
        dados = {}
        if produto:
            dados = {
                "nome": produto.nome,
                "url": produto.url or "",
                "preco_alvo": f"{produto.preco_alvo:.2f}".replace(".", ","),
                "loja_id": produto.loja_id,
                "categoria_id": produto.categoria_id,
            }
    return templates.TemplateResponse(
        request, "produto_form.html",
        {
            "produto": produto, "dados": dados, "erro": erro,
            "lojas": db.query(Loja).order_by(Loja.nome).all(),
            "categorias": db.query(Categoria).order_by(Categoria.nome).all(),
        },
        status_code=status,
    )


def _detalhe(request: Request, produto: Produto, erro: str | None = None, status: int = 200):
    return templates.TemplateResponse(
        request, "produto_detalhe.html",
        {
            "produto": produto, "erro": erro,
            "preco_atual": preco_atual(produto),
            "menor_preco": menor_preco(produto),
            "em_promocao": em_promocao(produto),
        },
        status_code=status,
    )


def _salvar(request: Request, db: Session, produto: Produto | None, nome: str, url: str,
            preco_alvo: str, loja_id: str, categoria_id: str):
    dados = {"nome": nome, "url": url, "preco_alvo": preco_alvo,
             "loja_id": _para_int(loja_id), "categoria_id": _para_int(categoria_id)}
    nome = nome.strip()
    if not nome:
        return _formulario(request, db, produto, dados, MSG_NOME, 400)
    try:
        alvo = parse_preco(preco_alvo)
    except ValueError as e:
        return _formulario(request, db, produto, dados, str(e), 400)
    loja = db.get(Loja, dados["loja_id"]) if dados["loja_id"] else None
    categoria = db.get(Categoria, dados["categoria_id"]) if dados["categoria_id"] else None
    if loja is None or categoria is None:
        return _formulario(request, db, produto, dados, MSG_VINCULO, 400)

    produto = produto or Produto()
    produto.nome = nome
    produto.url = url.strip() or None
    produto.preco_alvo = alvo
    produto.loja = loja
    produto.categoria = categoria
    db.add(produto)
    db.commit()
    return RedirectResponse(f"/produtos/{produto.id}", status_code=303)


@router.get("/produtos")
def listar(request: Request, db: Session = Depends(get_db)):
    produtos = db.query(Produto).order_by(Produto.nome).all()
    linhas = [
        {"produto": p, "preco_atual": preco_atual(p), "em_promocao": em_promocao(p)}
        for p in produtos
    ]
    return templates.TemplateResponse(request, "produtos.html", {"linhas": linhas})


@router.get("/produtos/novo")
def novo_form(request: Request, db: Session = Depends(get_db)):
    return _formulario(request, db, None)


@router.post("/produtos")
def criar(request: Request, nome: str = Form(""), url: str = Form(""),
          preco_alvo: str = Form(""), loja_id: str = Form(""), categoria_id: str = Form(""),
          db: Session = Depends(get_db)):
    return _salvar(request, db, None, nome, url, preco_alvo, loja_id, categoria_id)


@router.get("/produtos/{produto_id}")
def detalhe(produto_id: int, request: Request, db: Session = Depends(get_db)):
    return _detalhe(request, _buscar(db, produto_id))


@router.get("/produtos/{produto_id}/editar")
def editar_form(produto_id: int, request: Request, db: Session = Depends(get_db)):
    return _formulario(request, db, _buscar(db, produto_id))


@router.post("/produtos/{produto_id}/editar")
def editar(produto_id: int, request: Request, nome: str = Form(""), url: str = Form(""),
           preco_alvo: str = Form(""), loja_id: str = Form(""), categoria_id: str = Form(""),
           db: Session = Depends(get_db)):
    produto = _buscar(db, produto_id)
    return _salvar(request, db, produto, nome, url, preco_alvo, loja_id, categoria_id)


@router.post("/produtos/{produto_id}/excluir")
def excluir(produto_id: int, db: Session = Depends(get_db)):
    db.delete(_buscar(db, produto_id))
    db.commit()
    return RedirectResponse("/produtos", status_code=303)


@router.post("/produtos/{produto_id}/precos")
def registrar_preco(produto_id: int, request: Request, preco: str = Form(""),
                    db: Session = Depends(get_db)):
    produto = _buscar(db, produto_id)
    try:
        valor = parse_preco(preco)
    except ValueError as e:
        return _detalhe(request, produto, str(e), 400)
    produto.historico.append(HistoricoPreco(preco=valor))
    db.commit()
    return RedirectResponse(f"/produtos/{produto_id}", status_code=303)


@router.post("/precos/{historico_id}/excluir")
def excluir_preco(historico_id: int, db: Session = Depends(get_db)):
    registro = db.get(HistoricoPreco, historico_id)
    if registro is None:
        raise HTTPException(status_code=404, detail="Registro de preço não encontrado.")
    produto_id = registro.produto_id
    db.delete(registro)
    db.commit()
    return RedirectResponse(f"/produtos/{produto_id}", status_code=303)
