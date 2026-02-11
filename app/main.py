from fastapi import FastAPI
from app.api.routes import startup, users, admin, expenses
from app.initial_data import create_first_admin
from app.seed import seed_data


app = FastAPI(title="Fintrack API", version="0.1.0")
create_first_admin()


app.include_router(startup.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(expenses.router)

