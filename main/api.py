from ninja import Router
from ninja.security import HttpBearer
from rest_framework.authtoken.models import Token
from .models import Genre, Author
from graphene_django.views import GraphQLView
from .Schema import schema as graphql_schema  # Import your GraphQL schema from schema.py

# Security class for Bearer Authentication
class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            user_token = Token.objects.get(key=token)
            request.user = user_token.user
            return user_token.user
        except Token.DoesNotExist:
            return None


# Define REST API routes
router = Router()


@router.get("/genres", auth=BearerAuth())
def list_genres(request):
    """List all genres."""
    return Genre.objects.all()


@router.get("/authors", auth=BearerAuth())
def list_authors(request):
    """List all authors."""
    return Author.objects.all()
