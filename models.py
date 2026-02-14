from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

# conexãop do banco de dados
db = create_engine('sqlite:///database.db', echo=True)

# cria a base do banco de dados
Base = declarative_base()

# criar as classes/tabelas
# usuário
# pedido
# itensPedido
# novas tabelas
# endereco, estabelecimento, categoria


class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String, unique=True, nullable=False)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = 'pedidos'

    # STATUS_PEDIDO = [
    #     ('PENDENTE', 'Pendente'),
    #     ('EM_PREPARACAO', 'Em Preparação'),
    #     ('PRONTO', 'Pronto'),
    #     ('ENTREGUE', 'Entregue'),
    #     ('CANCELADO', 'Cancelado')
    # ]

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String, nullable=False)
    usuario = Column("usuario", Integer, ForeignKey('usuarios.id'), nullable=False)
    total = Column("total", Float, nullable=False)

    def __init__(self, usuario, status='PENDENTE', total=0):
        self.status = status
        self.usuario = usuario
        self.total = total

class ItemPedido(Base):
    __tablename__ = 'itens_pedido'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer, nullable=False)
    sabor = Column("sabor", String(50), nullable=False)
    tamanho = Column("tamanho", String(20), nullable=False)
    preco_unitario = Column("preco_unitario", Float, nullable=False)
    pedido = Column("pedido", Integer, ForeignKey('pedidos.id'), nullable=False)

    def __init__(self, pedido, quantidade, sabor, tamanho, preco_unitario):
        self.pedido = pedido
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario

# executa a criação dos metadados no banco de dados