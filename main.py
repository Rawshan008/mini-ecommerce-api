from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.users.routing import router as users_router
from auth.auth import router_api as auth_router
from database.config import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
  init_db()
  yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(auth_router, prefix="/api/auth", tags=['auth'])


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(host="127.0.0.1", port=8000)
