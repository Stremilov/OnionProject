from src.api.products import product_router
from src.api.orders import order_router

all_routers = [
    product_router,
    order_router,
]