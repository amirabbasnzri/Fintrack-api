from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from app.i18n.middleware import t
from app.schemas.i18n import LanguageSchema

router = APIRouter(tags=["i18n"], prefix="/i18n")


@router.post("/set-language/{lang}")
async def set_language(data: LanguageSchema, response: Response):
    response.set_cookie(key="lang", value=data.lang)
    return JSONResponse({"message": t("LANGUAGE_SAT", data.lang)})