from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from typing import List, TYPE_CHECKING
from api.categories.modules import CategoryBase, Category, CategoryCreate, CategoryUpdate, CategoryResponse
from database.config import get_session

if TYPE_CHECKING:
  from api.products.modules import Product

router = APIRouter()


# Show all Caterories 
@router.get('/', response_model=List[CategoryResponse])
async def category_all(
  skip: int = 0, 
  limit: int = 10, 
  session: Session = Depends(get_session)
):
  statement = select(Category).offset(skip).limit(limit)
  categories = session.exec(statement).all()
  return categories


# Create Categories 
@router.post('/create', status_code=status.HTTP_201_CREATED)
async def category_create(category: CategoryCreate, session: Session = Depends(get_session)):
  category_create = Category.model_validate(category)
  session.add(category_create)
  session.commit()
  session.refresh(category_create)
  return category_create


# Update Categories 
@router.put('/update/{cat_id}', status_code=status.HTTP_200_OK, response_model=CategoryResponse)
async def category_update(cat_id: int, cat_update: CategoryUpdate, session: Session = Depends(get_session)):
  category = session.get(Category, cat_id)
  if not category:
    raise HTTPException(status_code=404, detail="Category Not Found")
  new_cat = cat_update.model_dump(exclude_unset=True)
  for field, value in new_cat.items():
    setattr(category, field, value)
  session.add(category)
  session.commit()
  session.refresh(category)
  return category

# Single Category 
@router.get('/{cat_id}', response_model=CategoryResponse)
async def category_single(cat_id: int, session: Session = Depends(get_session)):
  category = session.get(Category, cat_id)
  if not category:
    raise HTTPException(status_code=404, detail="Category Not Found")
  return category

# Delte Category 
@router.delete('/{cat_id}')
async def category_delete(cat_id: int, session: Session = Depends(get_session)):
  category = session.get(Category, cat_id)
  if not category:
    raise HTTPException(status_code=404, detail="Category Not Found")
  session.delete(category)
  session.commit()
  return {
    "status": "Category Deleted Successfully"
  }