from fastapi import APIRouter, Query, HTTPException
from app.database import get_connection
from app.schemas.cliente import ClienteSchema
from typing import Optional

router = APIRouter(prefix="/v1/clientes")

@router.get("/")
def listar_clientes(s: Optional[str] = Query(None)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if s:
                like = f"%{s}%"
                cur.execute("SELECT id, cpf, nome FROM clientes WHERE cpf ILIKE %s OR nome ILIKE %s", (like, like))
            else:
                cur.execute("SELECT id, cpf, nome FROM clientes")
            clientes = cur.fetchall()
    return [{"id": c[0], "cpf": c[1], "nome": c[2]} for c in clientes]

@router.post("/")
def criar_cliente(cliente: ClienteSchema):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("INSERT INTO clientes (cpf, nome) VALUES (%s, %s)", (cliente.cpf, cliente.nome))
                conn.commit()
            except Exception:
                conn.rollback()
                raise HTTPException(status_code=400, detail="CPF já cadastrado.")
    return {"mensagem": "Cliente cadastrado com sucesso"}

@router.put("/{id_cliente}")
def atualizar_cliente(id_cliente: int, cliente: ClienteSchema):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM clientes WHERE id = %s", (id_cliente,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Cliente não encontrado")
            try:
                cur.execute("UPDATE clientes SET cpf = %s, nome = %s WHERE id = %s", (cliente.cpf, cliente.nome, id_cliente))
                conn.commit()
            except Exception:
                conn.rollback()
                raise HTTPException(status_code=400, detail="CPF já cadastrado.")
    return {"mensagem": "Cliente atualizado com sucesso"}
