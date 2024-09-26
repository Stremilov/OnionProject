from datetime import datetime

from pydantic import BaseModel


class UpdateOrderStatusSchema(BaseModel):
    status: str


class CreateOrderSchema(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class OrderResponseSchema(BaseModel):
    id: int
    created_at: datetime
    status: str
    product_id: int
    quantity: int
