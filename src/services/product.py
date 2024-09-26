from src.utils.repository import AbstractRepository

from src.schemas.products import CreateProductSchema


class ProductService():
    def __init__(self, products_repo: AbstractRepository):
        self.products_repo: AbstractRepository = products_repo()

    async def add_product(self, product: CreateProductSchema):
        product_dict = product.model_dump()
        product_id = await self.products_repo.add_one(product_dict)
        return product_id

    async def get_products(self):
        products = await self.products_repo.find_all()
        return products

    async def get_product_info(self, id: int):
        product_info = await self.products_repo.find_by_id(id)
        return product_info

    async def update_info(self, id: int, new_data: dict):
        result = await self.products_repo.update_info(id, new_data)
        return result

    async def delete_item(self, id):
        result = await self.products_repo.delete_item(id)
        return result
