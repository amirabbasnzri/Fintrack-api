from fastapi import FastAPI
from app.api.routes import auth



app = FastAPI(title="Fintrack API", version="0.1.0")


app.include_router(auth.router)