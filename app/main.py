from fastapi import FastAPI
from app.routers import produtos, estoque, clientes, relatorios

app = FastAPI()

app.include_router(produtos.router)
app.include_router(estoque.router)
app.include_router(clientes.router)
app.include_router(relatorios.router)

