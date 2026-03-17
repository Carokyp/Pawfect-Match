"""URL configuration for the pawfect_match project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import (
    home,
    register,
    login_view,
    forgot_password,
)

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("sign-in/", login_view, name="sign_in"),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("connections/", include("connections.urls")),
    path("dogs/", include("dogs.urls")),
    path("messages/", include("messaging.urls")),
    path("password-reset/", forgot_password, name="password_reset"),
    path("profiles/", include("profiles.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

# Custom error handlers
handler404 = "accounts.views.handler404"
handler500 = "accounts.views.handler500"
handler403 = "accounts.views.handler403"
handler405 = "accounts.views.handler405"
