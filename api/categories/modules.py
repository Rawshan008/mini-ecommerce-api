from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
  from api.products.modules import Product


class CategoryBase(SQLModel):
  name: str = Field(unique=True, index=True)
  description: Optional[str] = None

class Category(CategoryBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  products: list["Product"] = Relationship(back_populates="categories", cascade_delete=True)

class CategoryCreate(CategoryBase):
  pass

class CategoryUpdate(SQLModel):
  name: Optional[str] = None
  description: Optional[str] = None

class CategoryResponse(CategoryBase):
  id: int