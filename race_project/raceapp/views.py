import subprocess
import json
from django.shortcuts import render
from django.http import JsonResponse
import os


def run_scraper(request):
    try:
        # Run the Puppeteer script
        subprocess.run(["node", "raceapp/scraping/scrape_races.js"], check=True)

        # Define the path to the JSON file
        json_file_path = os.path.join("raceapp", "scraping", "race_data.json")

        # Check if the JSON file exists
        if not os.path.exists(json_file_path):
            return JsonResponse(
                {
                    "status": "error",
                    "error": "File not found: {}".format(json_file_path),
                }
            )

        # Read the data from the JSON file
        with open(json_file_path, "r") as file:
            race_data = json.load(file)

        return render(request, "raceapp/race_data.html", {"race_data": race_data})
    except subprocess.CalledProcessError as e:
        return JsonResponse({"status": "error", "error": str(e)})
    except FileNotFoundError as e:
        return JsonResponse({"status": "error", "error": str(e)})
