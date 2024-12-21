from django.urls import path
from .views import (
    home,
    run_scraper,
    save_race_data,
    display_race_data,
    get_progress,
    login_view,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", home, name="home"),
    path("run_scraper/", run_scraper, name="run_scraper"),
    path("save_race_data/", save_race_data, name="save_race_data"),
    path("display_race_data/", display_race_data, name="display_race_data"),
    path("get_progress/<str:task_id>/", get_progress, name="get_progress"),
    path("login/", login_view, name="login"),
    path(
        "logout/", auth_views.LogoutView.as_view(next_page="logged_out"), name="logout"
    ),  # Use Django's LogoutView
]

from django.urls import path
from .views import home, login_view
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path("", home, name="home"),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logged_out'), name='logout'),
    path('logged_out/', TemplateView.as_view(template_name='registration/logged_out.html'), name='logged_out'),
]
