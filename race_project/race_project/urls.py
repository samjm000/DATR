from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("raceapp/", include("raceapp.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "", lambda request: HttpResponseRedirect("/raceapp/")
    ),  # Ensure the redirect to raceapp
]
