from django.contrib import admin
from .models import Book, Author, BookReview, BookAuthor

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookReview)
admin.site.register(BookAuthor)
