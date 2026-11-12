# Monitor de Promoções

**Trabalho individual — Miguel Galvão Moreira da Silva**

Projeto das disciplinas **Projeto de Desenvolvimento de Software I e II** — UniFil (Centro Universitário Filadélfia), Londrina, 2026.

## Sobre o sistema

Aplicação web para acompanhar preços de produtos que você quer comprar. Para cada produto você define um
**preço-alvo** e registra os preços que encontra nas lojas. O sistema guarda o histórico e mostra,
na página inicial, os produtos **em promoção**: aqueles cujo último preço registrado está igual ou
abaixo do preço-alvo.

### Funcionalidades (casos de uso)

| Caso de uso | Descrição |
|---|---|
| UC01 Gerenciar Lojas | Cadastrar, listar, editar e excluir lojas |
| UC02 Gerenciar Categorias | Cadastrar, listar, editar e excluir categorias |
| UC03 Gerenciar Produtos | Cadastrar, listar, editar, excluir e ver detalhes de produtos |
| UC04 Registrar Preço | Registrar o preço encontrado e excluir registros do histórico |
| UC05 Consultar Promoções | Ver produtos com preço atual ≤ preço-alvo, economia e menor preço |

## Tecnologias

- Python 3.12
- FastAPI + Jinja2 (páginas HTML renderizadas no servidor)
- SQLAlchemy 2 (ORM) + SQLite (banco de dados relacional em arquivo)
- Pico.css (estilo)
- pytest (testes automatizados)

## Como executar

```bash
# 1. Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/macOS

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. (Opcional) Popular o banco com dados de exemplo
python seed.py

# 4. Iniciar o servidor
uvicorn app.main:app --reload
```

Acesse **http://localhost:8000**. A documentação automática da API (Swagger) fica em
http://localhost:8000/docs.

O banco `monitor.db` é criado automaticamente na primeira execução.

## Testes

```bash
pytest
```

## Estrutura

```
app/
  main.py          # cria a aplicação e registra as rotas
  database.py      # conexão com o SQLite
  models.py        # entidades: Loja, Categoria, Produto, HistoricoPreco
  services.py      # regras: preço atual, menor preço, promoções
  templating.py    # Jinja2 e formatação em Real (R$)
  routers/         # rotas de cada caso de uso
  templates/       # páginas HTML
tests/             # testes automatizados
seed.py            # dados de exemplo
docs/              # documentação (PDF) e diagramas UML
```

## Documentação

- [Documentação completa (PDF)](docs/Documentacao-Monitor-Promocoes.pdf)
- [Diagramas UML (fontes PlantUML)](docs/diagramas/)
