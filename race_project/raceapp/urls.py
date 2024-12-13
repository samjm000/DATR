# raceapp/urls.py
from django.urls import path
from . import views  # Import views from the current module

urlpatterns = [
    path("run-scraper/", views.run_scraper, name="run_scraper"),
]
