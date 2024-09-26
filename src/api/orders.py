from typing import Annotated

from fastapi import APIRouter, Depends
from src.api.dependencies import order_service

from src.schemas.orders import CreateOrderSchema
from src.services.order import OrderService


order_router = APIRouter(
    prefix="/order",
    tags=["Orders"]
)



@order_router.post("")
async def create_order(
        order_data: CreateOrderSchema,
        order_service: Annotated[OrderService, Depends(order_service)],

):
    order_id = await order_service.add_order(order_data)

    return {"order_id": order_id}


@order_router.get("")
async def get_orders(
        order_service: Annotated[OrderService, Depends(order_service)],
):
    orders = await order_service.get_orders()
    return {"orders": orders}


@order_router.get("/{id}")
async def get_order(
        id: int,
        order_service: Annotated[OrderService, Depends(order_service)],
):
    order_info = await order_service.get_order_info(id)
    return {"order": order_info}


@order_router.put("/{id}/status")
async def update_order(
        id: int,
        new_data: dict,
        order_service: Annotated[OrderService, Depends(order_service)],
):
    status = await order_service.update_info(id, new_data=new_data)
    return status