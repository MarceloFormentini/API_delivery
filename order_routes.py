from fastapi import APIRouter, HTTPException

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.get("/")
async def listar():
    """
    Essa é a rota padrão de pedidos do sistema. Ela pode ser usada para listar os pedidos existentes ou para verificar se a rota está funcionando corretamente. No futuro, essa rota pode ser expandida para incluir funcionalidades como criação, atualização e exclusão de pedidos, bem como a integração com um banco de dados para armazenar as informações dos pedidos.
    """
    return {
        "message": "Você acessou a rota padrão de ordem!"
    }