# Day at the races
# main.py

import requests
from bs4 import BeautifulSoup


# Example URL for today's races (this would need dynamic date handling)
race_url = "https://www.attheraces.com/racecards/tomorrow"


def get_race_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = get_races(url, headers)
    # response = requests.get(url, headers=headers)
    # soup = BeautifulSoup(response.text, "html.parser")
    return response


if __name__ == "__main__":
    print("running Scraper")
    print(get_race_data(race_url))
