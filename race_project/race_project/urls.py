# race_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("raceapp/", include("raceapp.urls")),
    path(
        "", lambda request: HttpResponseRedirect("/raceapp/run-scraper/")
    ),  # Redirect root to raceapp
]
