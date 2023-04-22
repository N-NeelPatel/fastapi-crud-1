from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class BookData(BaseModel):
    name: str
    edition: str
    publication_year: int
    authors: str
    author_id: int
