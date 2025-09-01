from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from api.products.modules import Product, ProductCreate, ProductUpdate, ProductResponse
from api.categories.modules import Category
from typing import List
from database.config import get_session

router = APIRouter()

# Get all products 
@router.get("/", response_model=List[ProductResponse])
async def product_all(
    skip: int = 0,
    limit: int = 15,
    session: Session = Depends(get_session)
  ):
  statement = select(Product).offset(skip).limit(limit)
  products = session.exec(statement).all()

  return products

# Create Posts 
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def product_create(product: ProductCreate, session: Session = Depends(get_session)):
  product_create = Product.model_validate(product)
  session.add(product_create)
  session.commit()
  session.refresh(product_create)
  return product_create;


# Single Product 
@router.get('/{product_id}', response_model=ProductResponse)
async def product_single(product_id: int, session: Session = Depends(get_session)):
  product = session.get(Product, product_id)
  if not product:
    raise HTTPException(status_code=404, detail="Product not Found")
  return product

# Update product
@router.put('/update/{product_id}', status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def product_update(product_id: int, product_update: ProductUpdate, session: Session = Depends(get_session)):
  product = session.get(Product, product_id)
  if not product:
    raise HTTPException(status_code=404, detail="Product Not Found!")
  new_product = product_update.model_dump(exclude_unset=True)
  for field, value in new_product.items():
    setattr(product, field, value)
  session.add(product)
  session.commit()
  session.refresh(product)
  return product

# Delete Product 
@router.delete("/delete/{product_id}")
async def product_delete(product_id: int, session: Session = Depends(get_session)):
  product = session.get(Product, product_id)
  if not product:
    raise HTTPException(status_code=404, detail="Product not Avilable!")
  session.delete(product)
  session.commit()
  return {
    "status": "product Delete Sucessfully"
  }