from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, logout_then_login

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("scores.urls", namespace="scores")),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", logout_then_login, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
