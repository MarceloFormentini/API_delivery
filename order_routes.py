from fastapi import APIRouter, Depends, HTTPException
from dependencies import getSession, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from sqlalchemy.orm import Session
from models import Pedido, Usuario, ItemPedido
from typing import List

order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verificar_token)])


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

@order_router.post("pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(getSession), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")

    pedido.status = "CANCELADO"
    pedido.commit()

    return{
        "mensagem": f"Pedido número {pedido.id} cancelado",
        "pedido": pedido
    }

@order_router.post("/listar")
async def listar_pedidos(session: Session = Depends(getSession), usuario: Usuario = Depends(verificar_token)):
    # if usuario.admin:
    #     pedidos = session.query(Pedido).all()
    # else:
    #     pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()

    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para acessar essa rota")

    pedidos = session.query(Pedido).all()
    return {
        "pedidos": pedidos
    }

@order_router.post("/pedido/adicionar_item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(getSession), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")

    item_pedido = ItemPedido(
        pedido=id_pedido,
        quantidade=item_pedido_schema.quantidade,
        sabor=item_pedido_schema.sabor,
        tamanho=item_pedido_schema.tamanho,
        preco_unitario=item_pedido_schema.preco_unitario
    )

    session.add(item_pedido)
    pedido.calcular_total()
    session.commit()

    return {
        "mensagem": f"Item adicionado ao pedido número {pedido.id}",
        "item_pedido": item_pedido.id,
        "pedido_total": pedido.total
    }

@order_router.post("/pedido/remover_item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, session: Session = Depends(getSession), usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()

    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item do pedido não encontrado")

    if not usuario.admin and usuario.id != item_pedido.pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")

    session.delete(item_pedido)
    pedido.calcular_total()
    session.commit()

    return {
        "mensagem": f"Item do pedido número {item_pedido.id} removido",
        "pedido_total": pedido.total,
        "itens_qtde": len(pedido.itens),
        "pedido": pedido
    }

@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(getSession), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")

    pedido.status = "FINALIZADO"
    session.commit()

    return {
        "mensagem": f"Pedido número {pedido.id} finalizado",
        "pedido": pedido
    }

@order_router.post("/pedido/{id_pedido}")
async def obter_pedido(id_pedido: int, session: Session = Depends(getSession), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para acessar essa rota")

    return {
        "qtde_itens": len(pedido.itens),
        "pedido": pedido
    }

@order_router.post("/listar/pedidos_usuario", response_model=List[ResponsePedidoSchema])
async def listar_pedidos_usuario(session: Session = Depends(getSession), usuario: Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()

    if not pedidos:
        raise HTTPException(status_code=400, detail="Nenhum pedido encontrado para este usuário")

    return pedidos