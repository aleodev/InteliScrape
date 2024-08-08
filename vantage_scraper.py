import httpx
import json
import os
from definitions import CONFIG_PATH, VANTAGE_API_KEY, ROOT_DIR
from utils import setup_config
import configparser

config = configparser.ConfigParser()


def run():
    # Config
    setup_config("vantage_scraper", {"NA": "N/A"})
    config.read(CONFIG_PATH)
    test_scrape()


def test_scrape():
    url = f"https://www.alphavantage.co/query?"
    response = httpx.get(
        url, params={"apikey": VANTAGE_API_KEY, "symbol": "IBM", "function": "OVERVIEW"}
    )
    print(f"Fetching ... \n")

    if response.status_code != 200:
        raise Exception("Failed to fetch!")

    # Parse & filter chunk
    json_data = response.json()
    filename = os.path.join(ROOT_DIR, "test.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
