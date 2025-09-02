import os
from fastapi import  Request
import  uuid
from sqlmodel import SQLModel, Session, create_engine

os.makedirs("storedata", exist_ok=True)

engine = create_engine("sqlite:///storedata/miniecommerce.db")

def init_db():
  SQLModel.metadata.create_all(engine)


def get_session():
  with Session(engine) as session:
    yield session


def get_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id