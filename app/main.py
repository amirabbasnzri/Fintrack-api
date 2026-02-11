from fastapi import FastAPI
from app.api.routes import users, admin
from app.initial_data import create_first_admin


app = FastAPI(title="Fintrack API", version="0.1.0")
create_first_admin()



app.include_router(users.router)
app.include_router(admin.router)