from ninja import Schema
from typing import Optional, List

class GenreSchema(Schema):
    id: int
    name: str

class AuthorSchema(Schema):
    id: int
    first_name: str
    last_name: str
    date_of_birth: Optional[str]  # Change to string to ensure proper validation
    date_of_death: Optional[str]  # Change to string to ensure proper validation

class BookSchema(Schema):
    id: int
    title: str
    author: AuthorSchema
    genre: List[GenreSchema]
    isbn: str
    summary: str
    copies_available: int
    file: str
