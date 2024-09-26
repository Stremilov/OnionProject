from select import select
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import update

from src.api.dependencies import product_service
from src.schemas.products import CreateProductSchema
from src.services.product import ProductService

product_router = APIRouter(prefix="/products", tags=["Products"])


@product_router.post("")
async def create_product(
    product_data: CreateProductSchema,
    product_service: Annotated[ProductService, Depends(product_service)],
):
    product_id = await product_service.add_product(product_data)
    return {"product_id": product_id}


@product_router.get("")
async def get_products(
    product_service: Annotated[ProductService, Depends(product_service)]
):
    products = await product_service.get_products()
    return {"products": products}


@product_router.get("/{id}")
async def get_products(
    id: int, product_service: Annotated[ProductService, Depends(product_service)]
):
    product_info = await product_service.get_product_info(id)
    return {"product_info": product_info}


@product_router.put("/{id}")
async def update_product(id: int, product_data: dict):
    result = await product_service().update_info(id=id, new_data=product_data)
    return result


@product_router.delete("/{id}")
async def delete_product(id: int):
    result = await product_service().delete_item(id=id)
    return result
