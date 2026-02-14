from fastapi import APIRouter, Depends, HTTPException
from dependencies import getSession
from models import Usuario
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do sistema. Ela pode ser usada para verificar se a rota está funcionando corretamente ou para testar a autenticação. No futuro, essa rota pode ser expandida para incluir funcionalidades como login, logout, registro de usuários e integração com um banco de dados para armazenar as informações dos usuários.
    """
    return {
        "message": "Você acessou a rota padrão de autenticação!", 
        "autenticado": False
    }

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(getSession)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    else:
        senha_criptografa = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(
            usuario_schema.nome, 
            usuario_schema.email, 
            senha_criptografa,
            usuario_schema.ativo,
            usuario_schema.admin
        )
        session.add(novo_usuario)
        session.commit()
        return {"message": f"Usuário {usuario_schema.nome} criado com sucesso!"}