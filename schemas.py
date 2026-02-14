from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    # define que é uma classe de configuração para o Pydantic, 
    # permitindo que os modelos sejam criados a partir de atributos 
    # de classe, em vez de apenas dicionários. Isso facilita a criação 
    # de instâncias do modelo usando argumentos nomeados, 
    # tornando o código mais legível e fácil de usar.
    class Config:
        from_attributes = True


class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True