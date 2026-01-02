from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from .views import LandingPageView


urlpatterns = [
    path("users/", include("users.urls")),
    path("books/", include("books.urls")),
    path("admin/", admin.site.urls),
    path("", LandingPageView.as_view(), name="landing_page"),
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
