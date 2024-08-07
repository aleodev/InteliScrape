import time
import httpx
import json
from constants import subreddits


def grabber():
    # Capped at last 500 posts per sub for now
    # Anything past 3 times per 100, the 4th is blank for some reason???
    # Should probably make scheduler

    for sub in subreddits:
        print(f"Fetching ${sub} \n")
        grab_sub(sub, 100, 4)


def grab_sub(sub, posts, rate):
    # Data
    dataset = []

    # Grab chunk past ID
    after_post_id = None

    # Retrieval point for any subreddit
    category = "hot"
    url = f"https://www.reddit.com/r/{sub}/{category}.json"

    for _ in range(rate):
        params = {"limit": posts, "t": "year", "after": after_post_id}  # time units
        response = httpx.get(url, params=params)

        print(f'Fetching chunk {_} "{response.url}"... \n')

        if response.status_code != 200:
            raise Exception("Failed to fetch!")

        json_data = response.json()

        parsed = [rec["data"] for rec in json_data["data"]["children"]]
        keys = ["title", "url"]
        filtered = [{key: item[key] for key in keys} for item in parsed]

        dataset.extend(filtered)

        # Set ID to grab next chunk
        after_post_id = json_data["data"]["after"]
        time.sleep(0.5)

    with open(f"export/{sub}.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)


def main():
    grabber()


main()
