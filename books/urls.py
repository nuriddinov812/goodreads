from books.views import BookListView, BookDetailView, AddBookReviewView, AddBookView, DeleteBookView, EditBookReviewView, DeleteBookReviewView
from django.urls import path


urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("<int:pk>/review/", AddBookReviewView.as_view(), name="add_book_review"),
    path("add/", AddBookView.as_view(), name="add_book"),
    path("<int:pk>/delete/", DeleteBookView.as_view(), name="delete_book"),
    path("review/<int:pk>/edit/", EditBookReviewView.as_view(), name="edit_book_review"),
    path("review/<int:pk>/delete/", DeleteBookReviewView.as_view(), name="delete_book_review"),
]
