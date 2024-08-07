import os
import time
import httpx
import json
from constants import subreddits
from utils import flatten_comments, group_comments


def scraper():
    # Capped at last 500 posts per sub for now
    # Anything past 3 times per 100, the 4th is blank for some reason???
    # Should probably make scheduler

    for sub in subreddits:
        print(f"Fetching ${sub} \n")

        # Scrape posts
        post_data = scrape_posts(sub)

        # Scrape comments using post data
        comment_data = scrape_comments(post_data)


def scrape_posts(subName):
    # Params
    postLimit = 100
    postRate = 1
    # Data
    dataset = []
    # Grab chunk past ID
    after_post_id = None

    # Retrieval point for any subreddit
    category = "hot"
    url = f"https://www.reddit.com/r/{subName}/{category}.json"

    for _ in range(postRate):
        # Fetch chunk
        params = {"limit": postLimit, "t": "year", "after": after_post_id}  # time units
        response = httpx.get(url, params=params)

        print(f'Fetching chunk {_} "{response.url}"... \n')

        if response.status_code != 200:
            raise Exception("Failed to fetch!")
        
        # Parse & filter chunk
        json_data = response.json()
        parsed = [rec["data"] for rec in json_data["data"]["children"]]
        
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
    filename = f"export/{subName}/index.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    return dataset


def scrape_comments(data):
    for post in data:
        # Fetch comments
        response = httpx.get(f'{post["url"]}.json')

        if response.status_code != 200:
            raise Exception("Failed to fetch!")

        # Parse comments
        json_data = response.json()
        parsed_data = json_data[1]["data"]["children"]
        
        # flat_data = list(flatten_comments(parsed_data))
        grouped_data = list(group_comments(parsed_data))

        # with open(f"export/flattened_comments.json", "w", encoding="utf-8") as f:
        #     json.dump(flat_data, f, indent=4, ensure_ascii=False)
        
        with open(f"export/{post["subreddit"]}/{post["id"]}.json", "w", encoding="utf-8") as f:
            json.dump(grouped_data, f, indent=4, ensure_ascii=False)




def test():

    response = httpx.get(
        "https://www.reddit.com/r/stocks/comments/1d5itn0/rate_my_portfolio_rstocks_quarterly_thread_june/.json"
    )

    if response.status_code != 200:
        raise Exception("Failed to fetch!")


def main():
    scraper()


main()
