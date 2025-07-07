from fastapi import APIRouter, HTTPException
from app.database import get_connection
from app.schemas.estoque import EstoqueEntradaSchema
from datetime import datetime

router = APIRouter(prefix="/v1/estoque")

@router.get("/produto/{codigo}/")
def entradas_produto(codigo: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM produtos WHERE codigo = %s", (codigo,))
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Produto não encontrado")
            produto_id = result[0]
            cur.execute("SELECT data_entrada, quantidade_entrada, valor_compra, valor_venda FROM estoque WHERE produto_id = %s", (produto_id,))
            entradas = cur.fetchall()
    return [{"data_entrada": str(e[0]), "quantidade_entrada": e[1], "valor_compra": float(e[2]), "valor_venda": float(e[3])} for e in entradas]

@router.post("/produto/{codigo}/")
def adicionar_entrada(codigo: str, entrada: EstoqueEntradaSchema):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM produtos WHERE codigo = %s", (codigo,))
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Produto não encontrado")
            produto_id = result[0]
            data = datetime.strptime(entrada.data_entrada, "%d/%m/%Y").date()
            cur.execute("""
                INSERT INTO estoque (produto_id, data_entrada, quantidade_entrada, valor_compra, valor_venda)
                VALUES (%s, %s, %s, %s, %s)
            """, (produto_id, data, entrada.quantidade_entrada, entrada.valor_compra, entrada.valor_venda))
            conn.commit()
    return {"mensagem": "Entrada de estoque registrada com sucesso"}
