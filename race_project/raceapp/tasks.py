# raceapp/tasks.py

from celery import shared_task
import subprocess
import json
import os
from .models import Racecard, Race, Horse


@shared_task(bind=True)
def scrape_and_save_data(self):
    try:
        subprocess.run(["node", "raceapp/scraping/scrape_races.js"], check=True)

        json_file_path = os.path.join("raceapp", "scraping", "race_data.json")
        if not os.path.exists(json_file_path):
            self.update_state(state="FAILURE", meta={"error": "File not found"})
            return {"status": "error", "error": "File not found"}

        with open(json_file_path, "r") as file:
            race_data = json.load(file)

        for racecard_data in race_data:
            racecard, _ = Racecard.objects.get_or_create(
                name=racecard_data["racecardName"]
            )
            for race_data in racecard_data["races"]:
                race, _ = Race.objects.get_or_create(
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
        return {"status": "success"}
    except subprocess.CalledProcessError as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        return {"status": "error", "error": str(e)}
    except FileNotFoundError as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        return {"status": "error", "error": str(e)}
