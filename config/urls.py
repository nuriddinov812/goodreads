from django.contrib import admin
from django.urls import path, include
from .views import LandingPageView


urlpatterns = [
    path("users/", include("users.urls")),
    path("books/", include("books.urls")),
    path("admin/", admin.site.urls),
    path("", LandingPageView.as_view(), name="landing_page"),
]
