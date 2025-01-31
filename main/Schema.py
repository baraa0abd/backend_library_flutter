import graphene
from graphene_django.types import DjangoObjectType
from .models import Genre, Author, Book
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.models import User
from datetime import datetime

# Define GraphQL Types
class GenreType(DjangoObjectType):
    class Meta:
        model = Genre
        fields = ("id", "name")

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name", "date_of_birth", "date_of_death")

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "genre",
            "isbn",
            "summary",
            "copies_available",
            "file",
            "image",
        )

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")

# Define Queries
class Query(graphene.ObjectType):
    all_genres = graphene.List(GenreType)
    all_authors = graphene.List(AuthorType)
    all_books = graphene.List(BookType)
    all_users = graphene.List(UserType)

    def resolve_all_genres(self, info):
        return Genre.objects.all()

    def resolve_all_authors(self, info):
        return Author.objects.all()

    def resolve_all_books(self, info):
        return Book.objects.prefetch_related("author", "genre").all()

    def resolve_all_users(self, info):
        return get_user_model().objects.all()

# Define Mutations
class CreateGenreMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(GenreType)

    def mutate(self, info, name):
        if not name.strip():
            raise Exception("Genre name cannot be empty")
        genre = Genre.objects.create(name=name)
        return CreateGenreMutation(genre=genre)

class CreateAuthorMutation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        date_of_birth = graphene.String()
        date_of_death = graphene.String()

    author = graphene.Field(AuthorType)

    def mutate(self, info, first_name, last_name, date_of_birth=None, date_of_death=None):
        try:
            if date_of_birth:
                datetime.strptime(date_of_birth, "%Y-%m-%d")
            if date_of_death:
                datetime.strptime(date_of_death, "%Y-%m-%d")
        except ValueError:
            raise Exception("Invalid date format. Use YYYY-MM-DD.")

        author = Author.objects.create(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            date_of_death=date_of_death,
        )
        return CreateAuthorMutation(author=author)

class CreateBookMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author_id = graphene.Int(required=True)
        genre_ids = graphene.List(graphene.Int, required=True)
        isbn = graphene.String(required=True)
        summary = graphene.String(required=True)
        copies_available = graphene.Int(required=True)
        file = graphene.String()

    book = graphene.Field(BookType)

    def mutate(self, info, title, author_id, genre_ids, isbn, summary, copies_available, file=None):
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            raise Exception("Author not found.")

        genres = Genre.objects.filter(id__in=genre_ids)
        if not genres.exists():
            raise Exception("No valid genres found.")

        book = Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            summary=summary,
            copies_available=copies_available,
            file=file,
        )
        book.genre.set(genres)
        return CreateBookMutation(book=book)

class SignUpMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, password):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return SignUpMutation(user=user)

class LoginMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(info.context, user)
            return LoginMutation(user=user)
        else:
            raise Exception("Invalid username or password")

# Combine all Mutations
class Mutation(graphene.ObjectType):
    create_genre = CreateGenreMutation.Field()
    create_author = CreateAuthorMutation.Field()
    create_book = CreateBookMutation.Field()
    signup = SignUpMutation.Field()
    login = LoginMutation.Field()

# Define the Schema
schema = graphene.Schema(query=Query, mutation=Mutation)