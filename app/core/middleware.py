from starlette.middleware.base import BaseHTTPMiddleware

class LanguageMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        lang = None

        query_lang = request.query_params.get("lang")
        cookie_lang = request.cookies.get("lang")
        header_lang = request.headers.get("accept-language")

        if query_lang:
            lang = query_lang
        elif cookie_lang:
            lang = cookie_lang
        elif header_lang:
            lang = header_lang.split(",")[0].split("-")[0]
        else:
            lang = "en"

        request.state.lang = lang
        response = await call_next(request)

        if query_lang and query_lang != cookie_lang:
            response.set_cookie("lang", lang, httponly=False)

        return response
