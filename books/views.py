from django.shortcuts import render

from django.views import View
from django.views.generic import ListView, DetailView
from books.models import Book

# Create your views here.


# class BooklistView(View):
#     def get(self, request):
#         books = Book.objects.all()

#         context = {
#             "books": books,
#         }
#         return render(request, "books/list.html", context)

class BookListView(ListView):
    
    template_name = "books/list.html"
    model = Book
    context_object_name = "books"


# class BookDetailView(View):
#     def get(self, request, pk):
#         book = Book.objects.get(pk=pk)
#         context = {
#             "book": book,
#         }
#         return render(request, "books/detail.html", context)

class BookDetailView(DetailView):
    template_name = "books/detail.html"
    pk_url_kwarg = "pk"
    model = Book

    
    
