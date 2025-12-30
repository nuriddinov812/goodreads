from books.views import BooklistView, BookDetailView
from django.urls import path


urlpatterns = [
    path("", BooklistView.as_view(), name="book_list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book_detail"),
]
