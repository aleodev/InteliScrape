import httpx
import json
import os
from definitions import CONFIG_PATH, VANTAGE_API_KEY, ROOT_DIR, STOCK
from utils import setup_config
import configparser

config = configparser.ConfigParser()


def run():
    # Config
    setup_config(
        "vantage_scraper",
        {
            "overview": "True",
            "income": "True",
            "balance": "True",
            "cashflow": "True",
            "earnings": "True",
        },
    )
    config.read(CONFIG_PATH)

    # Only setup for fundamentals
    print(f"Scraping {STOCK} ... \n")
    scrape_stock(STOCK)
    print("Scraping finished!")


def scrape_stock(stock):
    section = config["vantage_scraper"]
    options = [key for key, value in section.items() if json.loads(value.lower())]

    # Retrieval point
    for option in options:

        # Fetch data (doesn't like params for some reason)
        response = httpx.get(
            f"https://www.alphavantage.co/query?function={option.upper()}&symbol={stock}&apikey={VANTAGE_API_KEY}"
        )
        print(f"Fetching {option} data ... \n")

        if response.status_code != 200:
            raise Exception("Failed to fetch!")

        # Parse data
        json_data = response.json()

        # Export option data
        filename = os.path.join(ROOT_DIR, f"export/vantage/{stock}/{option}.json")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
