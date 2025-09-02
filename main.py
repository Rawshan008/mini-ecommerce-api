from contextlib import asynccontextmanager
from fastapi import FastAPI

from auth.auth import router_api as auth_router
from api.users.routing import router as users_router
from api.categories.routing import router as category_router
from api.products.routing import router as product_router
from api.cartitems.routing import router as cart_router
from database.config import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
  init_db()
  yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(category_router, prefix='/api/category', tags=["category"])
app.include_router(product_router, prefix="/api/products", tags=["products"])
app.include_router(cart_router, prefix="/api/cart", tags=["carts"])


if __name__ == "__main__":
  import uvicorn
  uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
