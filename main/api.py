from ninja import NinjaAPI
from typing import List, Dict
from .models import Genre, Author, Book
from ninja.security import HttpBearer
from rest_framework.authtoken.models import Token
from .Schema import *
from ninja import Router
# Security class for Bearer Authentication
class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            user_token = Token.objects.get(key=token)
            request.user = user_token.user
            return user_token.user
        except Token.DoesNotExist:
            return None

router = Router()



# Genre APIs
@router.get("/genres", response=List[GenreSchema], auth=BearerAuth())
def list_genres(request):
    return Genre.objects.all()

@router.post("/genres", response=GenreSchema, auth=BearerAuth())
def create_genre(request, name: str):
    genre = Genre.objects.create(name=name)
    return genre

# Author APIs
@router.get("/authors", response=List[AuthorSchema], auth=BearerAuth())
def list_authors(request):
    return Author.objects.all()

@router.post("/authors", response=AuthorSchema, auth=BearerAuth())
def create_author(request, first_name: str, last_name: str, date_of_birth: str = None, date_of_death: str = None):
    author = Author.objects.create(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        date_of_death=date_of_death
    )
    return author

# Book APIs
@router.get("/books", response=List[BookSchema], auth=BearerAuth())
def list_books(request):
    return Book.objects.prefetch_related('author', 'genre').all()

@router.post("/books", response=BookSchema, auth=BearerAuth())
def create_book(request, title: str, author_id: int, genre_ids: List[int], isbn: str, summary: str, copies_available: int, file: str):
    author = Author.objects.get(id=author_id)
    book = Book.objects.create(
        title=title,
        author=author,
        isbn=isbn,
        summary=summary,
        copies_available=copies_available,
        file=file
    )
    book.genre.set(Genre.objects.filter(id__in=genre_ids))
    return book
