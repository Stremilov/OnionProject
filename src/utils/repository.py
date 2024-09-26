from abc import ABC, abstractmethod
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import insert, select, update, delete

from src.db.db import async_session_maker
from src.models.Order import Order
from src.models.Product import Product


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id):
        raise NotImplementedError

    @abstractmethod
    async def update_info(self, id, new_data):
        raise NotImplementedError

    @abstractmethod
    async def delete_item(self, id):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None


    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()


    async def find_all(self):
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res


    async def find_by_id(self, id: int):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            result = res.scalar_one_or_none()
            return result

    async def update_info(self, id: int, new_data: dict):
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()

            if product is None:
                raise HTTPException(status_code=404, detail="Product not found")

            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**new_data)
            )

            await session.execute(stmt)
            await session.commit()
            return "Success"

    async def delete_item(self, id: int):
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id == id).returning()
            result = await session.execute(stmt)
            session.commit()
            return result