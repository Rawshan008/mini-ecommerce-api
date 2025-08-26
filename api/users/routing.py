from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List, Annotated
from database.config import get_session
from api.users.models import UsersResponse, Users, UsersCreate, UsersUpdate
from auth.utils import get_password_hash, get_current_user


router = APIRouter()


# Get All Users 
@router.get("/", response_model=List[UsersResponse])
async def users_read(
  skip: int = 0,
  limit: int = 10,
  session: Session = Depends(get_session)
):
  statement = select(Users).offset(skip).limit(limit)
  users = session.exec(statement).all()
  return users


# Create Users 
@router.post("/", status_code=status.HTTP_201_CREATED)
async def users_create(create_user: UsersCreate, session: Session = Depends(get_session), current_user: Users = Depends(get_current_user)):
  hashed_password = get_password_hash(create_user.hashed_password)
  user = Users(
    email=create_user.email,
    username=create_user.username,
    fullname=create_user.fullname,
    hashed_password=hashed_password
  )

  session.add(user)
  session.commit()
  session.refresh(user)
  return user


# Show Single User 
@router.get("/{user_id}", response_model=UsersResponse)
async def users_read(user_id: int, session: Session = Depends(get_session)):
  user = session.get(Users, user_id)
  if not user:
    raise HTTPException(status_code=404, detail="User Not Found")
  return user

# Update Users 
@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UsersResponse)
async def users_update(user_id: int, user_update: UsersUpdate, session: Session = Depends(get_session), current_user: Users = Depends(get_current_user)):
  user = session.get(Users, user_id)
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  
  user_new = user_update.model_dump(exclude_unset=True)
  for field, value in user_new.items():
    if value is not None:
      if field == 'hashed_password':
        setattr(user, 'hashed_password', get_password_hash(value))
      else:
        setattr(user, field, value)
  session.add(user)
  session.commit()
  session.refresh(user)
  return user


# Delete User 
@router.delete("/{user_id}")
async def users_delete(user_id: int, session: Session = Depends(get_session), current_user: Users = Depends(get_current_user)):
  user = session.get(Users, user_id)
  if not user:
    raise HTTPException(status_code=404, detail="User not Found")
  session.delete(user)
  session.commit()
  return {
    "status": "Delete User Successfully"
  }
