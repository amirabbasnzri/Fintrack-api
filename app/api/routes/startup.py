from fastapi import APIRouter
from app.seed import seed_data


router = APIRouter(tags=["Startup"])

@router.post("/startup-seed")
def startup_seed():
    seeded = seed_data()
    if seeded:
        return {"msg": "Database was empty. Admin and fake data created."}
    return {"msg": "Database already has admin. No changes made."}
