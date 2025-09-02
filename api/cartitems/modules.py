from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from api.products.modules import Product


class CartItemBase(SQLModel):
    product_id: int | None = Field(default=None, foreign_key="product.id")
    quantity: int = Field(default=1, ge=1)

class CartItem(CartItemBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")

    product: Optional[Product] = Relationship()

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(CartItemBase):
    product_id: Optional[int] = None
    quantity: Optional[int] = None

class CartItemResponse(CartItemBase):
    id: int

