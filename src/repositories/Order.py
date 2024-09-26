from src.models.Order import Order

from src.utils.repository import SQLAlchemyRepository


class OrderRepository(SQLAlchemyRepository):
    model = Order
