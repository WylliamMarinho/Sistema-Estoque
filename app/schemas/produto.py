from pydantic import BaseModel

class ProdutoSchema(BaseModel):
    codigo: str
    descricao: str
