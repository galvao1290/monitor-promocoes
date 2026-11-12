"""Popula o banco com dados de exemplo (usado na demonstração).

Uso: python seed.py
Só insere dados se o banco ainda não tiver nenhuma loja.
"""
from datetime import datetime, timedelta

from app.database import SessionLocal, init_db
from app.models import Categoria, HistoricoPreco, Loja, Produto

# (nome, loja, categoria, preço-alvo, [(preço, dias atrás), ...])
PRODUTOS = [
    ("Fone Bluetooth JBL Tune 520", "Amazon", "Eletrônicos", 200.0,
     [(279.90, 20), (249.90, 10), (189.90, 1)]),
    ("Smartwatch Xiaomi Band 9", "Mercado Livre", "Eletrônicos", 250.0,
     [(299.00, 15), (289.00, 3)]),
    ("Controle DualSense PS5", "Magazine Luiza", "Games", 380.0,
     [(449.00, 30), (399.00, 12), (369.90, 2)]),
    ("The Legend of Zelda: Tears of the Kingdom", "Amazon", "Games", 250.0,
     [(299.90, 8), (279.90, 1)]),
    ("Air Fryer Mondial 4L", "Magazine Luiza", "Casa", 350.0,
     [(429.90, 25), (379.90, 9), (329.90, 0)]),
    ("Cafeteira Nespresso Essenza Mini", "Mercado Livre", "Casa", 400.0,
     [(499.00, 14), (469.00, 4)]),
]


def popular() -> bool:
    init_db()
    db = SessionLocal()
    try:
        if db.query(Loja).count() > 0:
            print("Banco já possui dados. Nada foi inserido.")
            return False

        lojas = {
            "Amazon": Loja(nome="Amazon", site="https://www.amazon.com.br"),
            "Mercado Livre": Loja(nome="Mercado Livre", site="https://www.mercadolivre.com.br"),
            "Magazine Luiza": Loja(nome="Magazine Luiza", site="https://www.magazineluiza.com.br"),
        }
        categorias = {
            "Eletrônicos": Categoria(nome="Eletrônicos", descricao="Fones, relógios e acessórios"),
            "Games": Categoria(nome="Games", descricao="Jogos e acessórios para consoles"),
            "Casa": Categoria(nome="Casa", descricao="Eletrodomésticos e utilidades"),
        }
        agora = datetime.now()
        for nome, loja, categoria, alvo, precos in PRODUTOS:
            produto = Produto(nome=nome, preco_alvo=alvo,
                              loja=lojas[loja], categoria=categorias[categoria])
            for valor, dias in precos:
                produto.historico.append(
                    HistoricoPreco(preco=valor, data_registro=agora - timedelta(days=dias))
                )
            db.add(produto)
        db.commit()
        print(f"Inseridos: {len(lojas)} lojas, {len(categorias)} categorias, "
              f"{len(PRODUTOS)} produtos.")
        return True
    finally:
        db.close()


if __name__ == "__main__":
    popular()
