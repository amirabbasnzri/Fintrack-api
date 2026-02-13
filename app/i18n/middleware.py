from http.client import HTTPException
import json
import os
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

DEFAULT_LANG = "en"
TRANSLATION_DIR = os.path.dirname(__file__)
SUPPORTED_LANGS = ["en", "fa"]


class I18nAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        lang = request.cookies.get("lang", "en")
        try:
            response = await call_next(request)
        except HTTPException as e:
            if e.status_code == 401:
                raise HTTPException(status_code=401, detail=t("NOT_UNAUTHORIZED", lang))
            raise e
        return response
    

def t(key: str, lang: str = "en", **kwargs):
    import json, os
    try:
        with open(os.path.join(TRANSLATION_DIR, f"{lang}.json"), "r", encoding="utf-8") as f:
            translations = json.load(f)
    except FileNotFoundError:
        translations = {}

    text = translations.get(key, key)
    return text.format(**kwargs)
