from django.urls import path
from .views import BookReviewDetailAPIView, BookReviewListAPIView

urlpatterns = [
    path('reviews/<int:pk>/', BookReviewDetailAPIView.as_view(), name='book-review-detail'),
    path('reviews/', BookReviewListAPIView.as_view(), name='book-review-list'),
]
