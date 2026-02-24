from fastapi import APIRouter, Depends, HTTPException
from dependencies import getSession, verificar_token
from models import Usuario
from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """
    Função para criar um token JWT (JSON Web Token) para um usuário autenticado. 
    O token é criado com base no ID do usuário e tem um tempo de expiração definido
    por ACCESS_TOKEN_EXPIRE_MINUTES. A função utiliza a biblioteca jose para codificar
    o token com uma chave secreta (SECRET_KEY) e um algoritmo de criptografia (ALGORITHM).
    O token gerado pode ser usado para autenticar o usuário em rotas protegidas do sistema,
    permitindo que ele acesse recursos autorizados.
    """
    data_expericacao = datetime.now(timezone.utc) + duracao_token
    dic_info = {
        "sub": str(id_usuario),
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
    """
    Essa é a rota para criar uma nova conta de usuário. Ela recebe os dados do usuário, como nome, 
    email, senha, status de ativo e admin, e verifica se um usuário com o mesmo email já existe no 
    banco de dados. Se o usuário já existir, a função levanta uma exceção HTTP 400 (Bad Request) 
    indicando que o usuário já existe. Caso contrário, a senha fornecida é criptografada usando 
    bcrypt_context, um novo objeto de usuário é criado e adicionado ao banco de dados, e uma mensagem 
    de sucesso é retornada indicando que o usuário foi criado com sucesso.
    """
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
    """
    Essa é a rota para realizar o login de um usuário. Ela recebe as credenciais de email e senha,
    autentica o usuário usando a função autenticar_usuario e, se a autenticação for bem-sucedida,
    cria um token de acesso (access token) e um token de atualização (refresh token) para o usuário. 
    O access token tem uma duração limitada, enquanto o refresh token tem uma duração mais longa. 
    Ambos os tokens são retornados ao usuário, permitindo que ele acesse recursos protegidos do 
    sistema e atualize seu token de acesso quando necessário.
    """
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorreto.")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    
@auth_router.post("/login-form")
async def login_form(dados_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(getSession)):
    """
    Função para realizar o login de um usuário usando o OAuth2PasswordRequestForm, que é um formulário de 
    autenticação padrão para APIs. Ela recebe as credenciais de email e senha do formulário, autentica o 
    usuário usando a função autenticar_usuario e, se a autenticação for bem-sucedida, cria um token de 
    acesso (access token) para o usuário. O token é retornado ao usuário, permitindo que ele acesse recursos 
    protegidos do sistema.
    """
    usuario = autenticar_usuario(dados_form.username, dados_form.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorreto.")
    else:
        access_token = criar_token(usuario.id)

        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    
@auth_router.get("/refresh")
async def refresh_token(usuario: Usuario = Depends(verificar_token)):
    """
    Essa é a rota para atualizar o token de acesso (refresh token). Ela é usada para gerar um novo
    token de acesso válido para um usuário autenticado, permitindo que ele continue acessando recursos
    protegidos sem precisar fazer login novamente. A função verifica o token de acesso atual do usuário
    e, se for válido, cria um novo token de acesso com uma nova data de expiração. O novo token é 
    retornado ao usuário, permitindo que ele continue usando os recursos autorizados do sistema.
    """
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }