from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home,
    run_scraper,
    save_race_data,
    display_race_data,
    get_progress,
    login_view,
    register_view,
)

urlpatterns = [
    path("", home, name="home"),
    path("run_scraper/", run_scraper, name="run_scraper"),
    path("save_race_data/", save_race_data, name="save_race_data"),
    path("display_race_data/", display_race_data, name="display_race_data"),
    path("get_progress/<str:task_id>/", get_progress, name="get_progress"),
    path(
        "login/", login_view, name="login"
    ),  # Ensure login_view is correctly referenced
    path(
        "register/", register_view, name="register"
    ),  # Ensure register_view is correctly referenced
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),  # Add logout view
]
