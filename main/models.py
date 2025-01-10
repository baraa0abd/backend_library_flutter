from django.db import models
from django.contrib.auth.models import User

# Genre model
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Author model
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Book model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.ManyToManyField(Genre, related_name='books')
    isbn = models.CharField(max_length=13, unique=True, help_text='13 Character ISBN number')
    summary = models.TextField(max_length=1000, help_text='Brief description of the book')
    copies_available = models.PositiveIntegerField(default=1)
    file = models.FileField(upload_to="files")

    def __str__(self):
        return self.title