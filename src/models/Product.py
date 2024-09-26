from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    count: Mapped[int]

    order_items = relationship("OrderItem", back_populates="product")

    def to_read_model(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "count": self.count,
        }
