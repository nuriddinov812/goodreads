# from django.urls import path
from rest_framework.routers import DefaultRouter
from api.views import BookReviewViewSet

router = DefaultRouter()
router.register(r'reviews', BookReviewViewSet, basename='bookreview')
urlpatterns = router.urls


# urlpatterns = [
#     path('reviews/<int:pk>/', BookReviewDetailAPIView.as_view(), name='book-review-detail'),
#     path('reviews/', BookReviewListAPIView.as_view(), name='book-review-list'),
# ]
