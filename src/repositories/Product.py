from src.models.Product import Product

from src.utils.repository import SQLAlchemyRepository, AbstractRepository


class ProductRepository(SQLAlchemyRepository):
    model = Product