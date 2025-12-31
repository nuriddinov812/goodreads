from books.views import BookListView, BookDetailView, AddBookReviewView
from django.urls import path


urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("<int:pk>/review/", AddBookReviewView.as_view(), name="add_book_review"),
]
