from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from api.categories.modules import Category


class ProductBase(SQLModel):
  name: str = Field(default=None, unique=True, index=True)
  description: Optional[str] = None
  price: float = Field(gt=0)
  category_id: int | None = Field(default=None, foreign_key="category.id")


class Product(ProductBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  
  categories: Category | None = Relationship(back_populates="products")


class ProductCreate(ProductBase):
  pass


class ProductUpdate(SQLModel):
  name: Optional[str] = None
  description: Optional[str] = None
  price: Optional[float] = None
  category_id: Optional[int] = None


class ProductResponse(ProductBase):
  id: int
  categories: Optional[Category] = None