from books.views import BookListView, BookDetailView
from django.urls import path


urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book_detail"),
]
