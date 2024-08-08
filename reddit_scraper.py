import os
import time
import httpx
import json
from definitions import SUBS, CONFIG_PATH, ROOT_DIR
from utils import group_comments, setup_config
import configparser
config = configparser.ConfigParser()

def run():
    # Config
    setup_config("reddit_scraper", {"post_limit": "100", "post_rate": "1", "category": "hot"})
    config.read(CONFIG_PATH)
    
    # Capped at last 500 posts per sub for now
    # Anything past 3 times per 100, the 4th is blank for some reason???
    # Should probably make scheduler

    for sub in SUBS:
        print(f"Scraping r/{sub} \n")

        # Scrape posts
        post_data = scrape_posts(sub)

        # Scrape comments using post data
        scrape_comments(post_data)


def scrape_posts(subName):
    # Params
    post_limit = int(config.get("reddit_scraper",'post_limit'))
    post_rate = int(config.get("reddit_scraper",'post_rate'))
    category = config.get("reddit_scraper",'category')
    # Data
    dataset = []
    # Grab chunk past ID
    after_post_id = None

    # Retrieval point for any subreddit
    url = f"https://www.reddit.com/r/{subName}/{category}.json"

    for _ in range(post_rate):
        # Fetch chunk
        params = {"limit": post_limit, "t": "year", "after": after_post_id}  # time units
        response = httpx.get(url, params=params)
        print(f'Fetching chunk {_} ... \n')

        if response.status_code != 200:
            raise Exception("Failed to fetch!")
        
        # Parse & filter chunk
        json_data = response.json()
        parsed = [rec["data"] for rec in json_data["data"]["children"] if rec["data"].get("num_comments") not in [0, None]]
        
        keys = [
            "selftext",
            "id",
            "url",
            "subreddit",
            "title",
        ]
        filtered = [{key: item[key] for key in keys} for item in parsed]

        # Add chunk to dataset
        dataset.extend(filtered)

        # Set ID to grab next chunk
        after_post_id = json_data["data"]["after"]
        time.sleep(0.5)

    # Export list of sub links
    filename = os.path.join(ROOT_DIR, f"export/reddit/{subName}/index.json")
    os.makedirs(os.path.dirname(filename), exist_ok=True)    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    return dataset


def scrape_comments(data):
    print(f'Fetching posts... \n')
    for post in data:
        # Fetch comments
        response = httpx.get(f'{post["url"]}.json')

        if response.status_code != 200:
            raise Exception("Failed to fetch!")

        # Parse comments
        json_data = response.json()
        parsed_data = json_data[1]["data"]["children"]
        grouped_data = list(group_comments(parsed_data))
        
        filename = os.path.join(ROOT_DIR, f"export/reddit/{post["subreddit"]}/{post["id"]}.json")
        os.makedirs(os.path.dirname(filename), exist_ok=True)   
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(grouped_data, f, indent=4, ensure_ascii=False)

