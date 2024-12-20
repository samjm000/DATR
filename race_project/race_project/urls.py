from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "raceapp/", include("raceapp.urls")
    ),  # This includes URLs from the 'raceapp' app
    path(
        "", lambda request: HttpResponseRedirect("/raceapp/")
    ),  # Redirect to 'raceapp' by default
]
