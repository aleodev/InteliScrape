import os
from definitions import CONFIG_PATH
from utils import setup_config
import configparser

config = configparser.ConfigParser()


def run():
    # Config
    setup_config("vantage_scraper", {"NA": "N/A"})
    config.read(CONFIG_PATH)
