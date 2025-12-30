from django.shortcuts import render

from django.views import View
from books.models import Book

# Create your views here.


class BooklistView(View):
    def get(self, request):
        books = Book.objects.all()

        context = {
            "books": books,
        }
        return render(request, "books/list.html", context)


class BookDetailView(View):
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        context = {
            "book": book,
        }
        return render(request, "books/detail.html", context)
