from pydantic import BaseModel
from typing import Optional

class Industry(BaseModel):
    slug: str
    name: str
    description: Optional[str]

class Article(BaseModel):
    title: str
    industry: str
    source: str
    content: str