from fastapi import APIRouter, Query, HTTPException
from app.database import get_connection
from app.schemas.produto import ProdutoSchema
from typing import Optional

router = APIRouter(prefix="/v1/produtos")

@router.get("/")
def listar_produtos(s: Optional[str] = Query(None)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if s:
                like = f"%{s}%"
                cur.execute("SELECT id, codigo, descricao FROM produtos WHERE codigo ILIKE %s OR descricao ILIKE %s", (like, like))
            else:
                cur.execute("SELECT id, codigo, descricao FROM produtos")
            produtos = cur.fetchall()
    return [{"id": p[0], "codigo": p[1], "descricao": p[2]} for p in produtos]

@router.post("/")
def criar_produto(produto: ProdutoSchema):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("INSERT INTO produtos (codigo, descricao) VALUES (%s, %s)", (produto.codigo, produto.descricao))
                conn.commit()
            except Exception:
                conn.rollback()
                raise HTTPException(status_code=400, detail="Código já existente.")
    return {"mensagem": "Produto cadastrado com sucesso"}

@router.put("/{id_produto}")
def atualizar_produto(id_produto: int, produto: ProdutoSchema):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM produtos WHERE id = %s", (id_produto,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Produto não encontrado")
            try:
                cur.execute("UPDATE produtos SET codigo = %s, descricao = %s WHERE id = %s", (produto.codigo, produto.descricao, id_produto))
                conn.commit()
            except Exception:
                conn.rollback()
                raise HTTPException(status_code=400, detail="Código já existente.")
    return {"mensagem": "Produto atualizado com sucesso"}
