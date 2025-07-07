from pydantic import BaseModel

class EstoqueEntradaSchema(BaseModel):
    data_entrada: str  # Formato DD/MM/AAAA
    quantidade_entrada: int
    valor_compra: float
    valor_venda: float
