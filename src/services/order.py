from datetime import datetime

from fastapi import HTTPException, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session, async_session_maker
from src.models.Order import OrderItem
from src.utils.repository import AbstractRepository

from src.schemas.orders import CreateOrderSchema


class OrderService:
    def __init__(self, orders_repo: AbstractRepository, products_repo: AbstractRepository):
        self.orders_repo = orders_repo()
        self.products_repo = products_repo()

    async def add_order(self, order: CreateOrderSchema):
        order_data = order.dict()

        async with async_session_maker() as session:
            product = await self.products_repo.find_by_id(order_data['product_id'])
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            if product.count < order_data['quantity']:
                raise HTTPException(status_code=400, detail="Insufficient stock")

            new_quantity = product.count - order_data['quantity']
            await self.products_repo.update_info(product.id, {"count": new_quantity})

            order_dict = {
                "status": "в процессе",
                "created_at": datetime.utcnow(),
            }
            order_id = await self.orders_repo.add_one(order_dict)

            stmt = insert(OrderItem).values(
                order_id=order_id,
                product_id=order_data["product_id"],
                quantity=order_data["quantity"],
            )
            await session.execute(stmt)
            await session.commit()

        return order_id

    async def get_orders(self):
        orders = await self.orders_repo.find_all()
        return orders

    async def update_info(self, id: int, new_data: dict):
        result = await self.orders_repo.update_info(id, new_data)
        return result

    async def get_order_info(self, id: int):
        order_info = await self.orders_repo.find_by_id(id)
        return order_info