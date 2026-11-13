# Monitor de Promoções

Projeto de Desenvolvimento de Software I e II - UniFil

Aluno: Miguel Galvão Moreira da Silva (trabalho individual)

## Sobre

Sistema web pra acompanhar o preço de produtos que eu quero comprar. Cadastro o produto com um preço-alvo e vou registrando os preços que encontro nas lojas. Quando o último preço registrado fica igual ou abaixo do preço-alvo, o produto aparece na tela de promoções.

Tem CRUD de lojas, categorias, produtos e do histórico de preços.

## Tecnologias

- Python 3.12
- FastAPI
- Jinja2 (páginas HTML)
- SQLAlchemy
- SQLite
- Pico.css

## Como rodar

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload
```

Depois é só abrir http://localhost:8000

O `seed.py` é opcional, ele só coloca alguns dados de exemplo no banco. O banco (monitor.db) é criado sozinho na primeira vez que roda.

## Documentação

A documentação (requisitos, casos de uso, DER e diagramas) está em `docs/Documentacao-Monitor-Promocoes.pdf`.
