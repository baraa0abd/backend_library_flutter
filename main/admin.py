from django.contrib import admin
from .models import Genre, Author, Book

# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'date_of_birth', 'date_of_death')
    search_fields = ('first_name', 'last_name')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'isbn', 'copies_available')
    search_fields = ('title', 'isbn')
    list_filter = ('genre',)
