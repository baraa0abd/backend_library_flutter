from django.contrib import admin
from django.urls import path
from main.api import router  # Import the Ninja router
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from main.Schema import schema
 # Import the GraphQL schema

urlpatterns = [
    path("admin/", admin.site.urls),  # Django admin # RESTful APIs
    path(
        "graphql/",
        csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)),
        name="graphql",  # GraphQL endpoint with Playground enabled
    ),
]
