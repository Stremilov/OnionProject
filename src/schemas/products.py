from pydantic import BaseModel


class CreateProductSchema(BaseModel):
    name: str
    description: str
    price: float
    count: int

    class Config:
        from_attributes = True
