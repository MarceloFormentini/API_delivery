from fastapi import Depends, HTTPException
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from jose import JWTError, jwt

def getSession():
    """
    Função de dependência para obter uma sessão do banco de dados. 
    Ela é usada para garantir que a sessão seja criada e fechada 
    corretamente em cada solicitação. A função pode ser usada em 
    rotas que precisam acessar o banco de dados, garantindo que a 
    conexão seja gerenciada de forma eficiente e segura.
    """
    Session = sessionmaker(bind=db)
    session = Session()
    try:
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(getSession)):
    """
    Função para verificar a validade de um token JWT (JSON Web Token). Ela decodifica o token usando 
    a chave secreta (SECRET_KEY) e o algoritmo de criptografia (ALGORITHM) definidos no sistema. Se 
    o token for válido, a função extrai o ID do usuário (sub) do payload do token e consulta o banco
    de dados para encontrar o usuário correspondente. Se o usuário for encontrado, ele é retornado; 
    caso contrário, ou se o token for inválido, a função levanta uma exceção HTTP 401 (Unauthorized)
    indicando que o token é inválido.
    """
    try:
        payload_dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(payload_dict.get("sub"))
        if id_usuario is None:
            raise HTTPException(status_code=401, detail="Acesso inválido.")

        usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
        if not usuario:
            raise HTTPException(status_code=401, detail="Acesso inválido.")

        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso inválido.")