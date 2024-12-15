from django.urls import path
from .views import home, run_scraper, save_race_data, display_race_data, get_progress

urlpatterns = [
    path("", home, name="home"),
    path("run_scraper/", run_scraper, name="run_scraper"),
    path("save_race_data/", save_race_data, name="save_race_data"),
    path("display_race_data/", display_race_data, name="display_race_data"),
    path("get_progress/<str:task_id>/", get_progress, name="get_progress"),
]
