from pydantic import BaseModel

class UrlGettter(BaseModel):
    title: str
    url: str