"""Ponto de entrada da aplicação Monitor de Promoções."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import categorias, lojas, produtos


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Monitor de Promoções", lifespan=lifespan)

app.include_router(lojas.router)
app.include_router(categorias.router)
app.include_router(produtos.router)
