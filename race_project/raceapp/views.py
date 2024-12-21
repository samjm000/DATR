# raceapp/views.py
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Racecard, Race, Horse
from .tasks import scrape_and_save_data
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                error_message = "Invalid login credentials. Please try again."
                form = AuthenticationForm()
                return render(
                    request,
                    "registration/login.html",
                    {"form": form, "error_message": error_message},
                )
        else:
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if password1 and password2 and password1 == password2:
                user = User.objects.create_user(
                    username=email, email=email, password=password1
                )
                user.save()
                user = authenticate(username=email, password=password1)
                if user is not None:
                    login(request, user)
                    return redirect("home")
            else:
                error_message = (
                    "Passwords do not match or are not provided. Please try again."
                )
                form = UserCreationForm()
                return render(
                    request,
                    "registration/login.html",
                    {"form": form, "error_message": error_message},
                )
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def home(request):
    return render(request, "home.html")


def run_scraper(request):
    if request.method == "GET":
        task = scrape_and_save_data.apply_async()  # Start the Celery task
        return render(request, "loading.html", {"task_id": task.id})


def get_progress(request, task_id):
    task = scrape_and_save_data.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {"state": task.state, "progress": 0, "status": "Pending..."}
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "progress": 100 if task.state == "SUCCESS" else 50,
            "status": str(task.info),
        }
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        response = {
            "state": task.state,
            "progress": 0,
            "status": str(task.info),  # This is the exception raised
        }
    return JsonResponse(response)


def save_race_data(request, data=None):
    if request.method == "POST" or data:
        if not data:
            data = json.loads(request.body)
        for racecard_data in data:
            racecard, created = Racecard.objects.get_or_create(
                name=racecard_data["racecardName"]
            )
            for race_data in racecard_data["races"]:
                race, created = Race.objects.get_or_create(
                    racecard=racecard,
                    link=race_data["link"],
                    title=race_data["title"],
                    details=race_data["details"],
                )
                for horse_data in race_data["horses"]:
                    Horse.objects.get_or_create(
                        race=race,
                        name=horse_data["name"],
                        link=horse_data["link"],
                        sire=horse_data.get("sire", ""),
                        dam=horse_data.get("dam", ""),
                        dams_sire=horse_data.get("damsSire", ""),
                    )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)


def display_race_data(request):
    racecards = Racecard.objects.all().prefetch_related("races__horses")
    return render(request, "raceapp/display_race_data.html", {"racecards": racecards})
