from fastapi import APIRouter, Depends, HTTPException
from dependencies import getSession
from schemas import PedidoSchema
from sqlalchemy.orm import Session
from models import Pedido

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.get("/")
async def pedidos():
    """
    Essa é a rota padrão de pedidos do sistema. Ela pode ser usada para listar os pedidos existentes ou para verificar se a rota está funcionando corretamente. No futuro, essa rota pode ser expandida para incluir funcionalidades como criação, atualização e exclusão de pedidos, bem como a integração com um banco de dados para armazenar as informações dos pedidos.
    """
    return {
        "message": "Você acessou a rota padrão de ordem!"
    }

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(getSession)):
    """
    Essa é a rota para criar um novo pedido. Ela pode ser usada para receber os detalhes do pedido, como os itens, 
    quantidades e informações do cliente, e processar a criação do pedido no sistema. No futuro, essa rota pode ser 
    expandida para incluir validação dos dados de entrada, integração com um banco de dados para armazenar as 
    informações do pedido e lógica adicional para calcular o total do pedido ou verificar a disponibilidade dos itens.
    """
    novo_pedido = Pedido(
        usuario=pedido_schema.usuario
    )

    session.add(novo_pedido)
    session.commit()
    return {
        "message": f"Pedido criado com sucesso para o usuário {pedido_schema.usuario}!",
        "pedido_id": novo_pedido.id
    }