from fastapi import Depends

from src.repositories.Order import OrderRepository
from src.repositories.Product import ProductRepository
from src.services.product import ProductService
from src.services.order import OrderService


def product_service():
    return ProductService(ProductRepository)


def order_service():
    return OrderService(OrderRepository, ProductRepository)
