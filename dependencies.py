from models import db
from sqlalchemy.orm import sessionmaker

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