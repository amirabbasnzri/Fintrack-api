from pydantic import BaseModel,  Field
from typing import Literal

class LanguageSchema(BaseModel):
    lang: Literal["fa", "en"] = Field(..., json_schema_extra={"example": "fa"})

