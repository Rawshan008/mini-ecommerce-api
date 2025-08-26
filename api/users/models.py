from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr

# Base Model Table
class UsersBase(SQLModel):
  email: EmailStr = Field(unique=True, index=True)
  username: str = Field(unique=True, index=True)
  fullname: str = Field(index=True)
  hashed_password: str

# User Main Table 
class Users(UsersBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)


# Create User Model 
class UsersCreate(UsersBase):
  pass


# Update User Model 
class UsersUpdate(SQLModel):
  email: Optional[EmailStr] = None
  username: Optional[str] = None
  hashed_password: Optional[str] = None


# Response Model 
class UsersResponse(UsersBase):
  id: int