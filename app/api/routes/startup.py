from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.seed import seed_data
from app.i18n.middleware import t


router = APIRouter(tags=["Startup"])


@router.post("/startup-seed")
def startup_seed():
    seeded = seed_data()
    if seeded:
        return JSONResponse(content={'msg': t("DB_SEEDED")}, status_code=200)
    return JSONResponse(content={"msg": t("DB_ALREADY_SEEDED")}, status_code=200)