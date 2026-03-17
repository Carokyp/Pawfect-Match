"""
URL configuration for pawfect_match project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
