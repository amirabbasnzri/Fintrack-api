import json
from pathlib import Path
from threading import Lock

BASE_PATH = Path(__file__).resolve().parent.parent / "locales"

_cache = {}
_lock = Lock()

def load_lang(lang: str):
    with _lock:
        if lang in _cache:
            return _cache[lang]

        file_path = BASE_PATH / f"{lang}.json"
        if not file_path.exists():
            file_path = BASE_PATH / "en.json"
            lang = "en"

        with open(file_path, encoding="utf-8") as f:
            _cache[lang] = json.load(f)
        return _cache[lang]

def t(key: str, lang: str = "en"):
    data = load_lang(lang)
    if key in data:
        return data[key]
    if lang != "en":
        data_en = load_lang("en")
        if key in data_en:
            return data_en[key]
    return key
