from pydantic import BaseModel

class ClienteSchema(BaseModel):
    cpf: str
    nome: str
