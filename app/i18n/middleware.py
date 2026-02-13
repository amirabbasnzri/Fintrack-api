import json
import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

DEFAULT_LANG = "en"
TRANSLATION_DIR = os.path.dirname(__file__)
SUPPORTED_LANGS = ["en", "fa"]

class I18nMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        lang = request.cookies.get("lang", DEFAULT_LANG)
        if lang not in SUPPORTED_LANGS:
            lang = DEFAULT_LANG
        request.state.lang = lang
        response: Response = await call_next(request)
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
