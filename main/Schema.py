from typing import List, Dict
from ninja import Schema

class GenreSchema(Schema):
    id: int
    name: str

class AuthorSchema(Schema):
    id: int
    first_name: str
    last_name: str
    date_of_birth: str = None
    date_of_death: str = None

class BookSchema(Schema):
    id: int
    title: str
    author: AuthorSchema
    genre: List[GenreSchema]
    isbn: str
    summary: str
    copies_available: int
    file: str