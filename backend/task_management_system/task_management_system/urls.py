from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Account API prefix endpoint
    path("api/account/", include("accounts.urls")),
]
