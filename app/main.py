"""Ponto de entrada da aplicação Monitor de Promoções."""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routers import categorias, lojas, produtos, promocoes


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Monitor de Promoções", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

app.include_router(promocoes.router)
app.include_router(lojas.router)
app.include_router(categorias.router)
app.include_router(produtos.router)
