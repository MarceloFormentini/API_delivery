from fastapi import APIRouter, Depends, HTTPException
from dependencies import getSession
from models import Usuario
from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario):
    """
    Função para criar um token JWT (JSON Web Token) para um usuário autenticado. 
    O token é criado com base no ID do usuário e tem um tempo de expiração definido
    por ACCESS_TOKEN_EXPIRE_MINUTES. A função utiliza a biblioteca jose para codificar
    o token com uma chave secreta (SECRET_KEY) e um algoritmo de criptografia (ALGORITHM).
    O token gerado pode ser usado para autenticar o usuário em rotas protegidas do sistema,
    permitindo que ele acesse recursos autorizados.
    """
    data_expericacao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dic_info = {
        "sub": id_usuario,
        "exp": data_expericacao
    }
    encode_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return encode_jwt    

def autenticar_usuario(email, senha, session):
    """
    Função para autenticar um usuário com base no email e senha fornecidos.
    Ela consulta o banco de dados para encontrar um usuário com o email
    correspondente e, em seguida, verifica se a senha fornecida corresponde
    à senha armazenada no banco de dados usando o bcrypt_context. Se a 
    autenticação for bem-sucedida, a função retorna o objeto do usuário;
    caso contrário, retorna False.
    """
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    else:
        return usuario


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
    
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(getSession)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorreto.")
    else:
        access_token = criar_token(usuario.id)

        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "message": f"Usuário {usuario.nome} autenticado com sucesso!"
        }