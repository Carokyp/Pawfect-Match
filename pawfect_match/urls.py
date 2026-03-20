"""URL configuration for the pawfect_match project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from accounts.views import (
    home,
    register,
    login_view,
    forgot_password,
    trigger_error,
)

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("sign-in/", login_view, name="sign_in"),
    path("accounts/", include("accounts.urls")),
    path(
        "admin/connections/connection/",
        RedirectView.as_view(url="/admin/connections/like/", permanent=False),
        name="admin_connection_legacy_redirect",
    ),
    path("admin/", admin.site.urls),
    path("connections/", include("connections.urls")),
    path("dogs/", include("dogs.urls")),
    path("messages/", include("messaging.urls")),
    path("password-reset/", forgot_password, name="password_reset"),
    path("profiles/", include("profiles.urls")),
    path("errors/403/", trigger_error, {"code": 403}, name="trigger_403"),
    path("errors/404/", trigger_error, {"code": 404}, name="trigger_404"),
    path("errors/405/", trigger_error, {"code": 405}, name="trigger_405"),
    path("errors/500/", trigger_error, {"code": 500}, name="trigger_500"),
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
