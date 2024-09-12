from pydantic import BaseModel


class Summary(BaseModel):
    url: str
