from passlib.context import CryptContext

from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
import os
from sqlmodel import Session, select
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.config import get_session
from auth.models import TokenData, Token
from api.users.models import Users, UsersResponse

SECRET_KEY = os.getenv('SECRET_KEY', "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = os.getenv('ALGORITHM', "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Varify Password 
def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)


# Hashed Password
def get_password_hash(password):
  return pwd_context.hash(password)

# user utility 
def get_user_by_username(username: str, session: Session ):
  return session.exec(select(Users).where(Users.username == username)).first()


# authentication 
def authenticate_user(username: str, password: str, session: Session):
    user = get_user_by_username(username, session)
    if not user:
       return False
    if not verify_password(password, user.hashed_password):
       return False
    return user


# Create Access Token 
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Get Current User 
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(token_data.username, session)
    if user is None:
        raise credentials_exception
    return user

# Get Active Users 
async def get_current_active_user(
    current_user: Annotated[Users, Depends(get_current_user)],
):
    if not current_user:
        raise HTTPException(status_code=400, detail="User not Found")
    return current_user