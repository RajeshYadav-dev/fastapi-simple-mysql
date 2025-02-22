from fastapi import FastAPI
from user.router import user_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app:FastAPI):
  print("SERVER STARTED....")
  yield
  print("SERVER STOPPED....")


version="v1"
app = FastAPI(
  title="REST API.",
  description="REST API for user web services.",
  version=version,
  lifespan=life_span
)
app.include_router(user_router,prefix=f"/api/{version}/users",tags=["user"])