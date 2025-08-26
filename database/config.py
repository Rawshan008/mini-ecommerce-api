import os
from sqlmodel import SQLModel, Session, create_engine

os.makedirs("storedata", exist_ok=True)

engine = create_engine("sqlite:///storedata/miniecommerce.db")

def init_db():
  SQLModel.metadata.create_all(engine)


def get_session():
  with Session(engine) as session:
    yield session