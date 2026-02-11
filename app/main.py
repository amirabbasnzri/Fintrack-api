from fastapi import FastAPI
from app.api.routes.users import router as user_router



app = FastAPI(title="Fintrack API", version="0.1.0")


app.include_router(user_router)