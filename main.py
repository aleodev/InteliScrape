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
        print(f"Scraping ${sub} \n")

        # Scrape posts
        post_data = scrape_posts(sub)

        # Scrape comments using post data
        scrape_comments(post_data)


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
    filename = f"export/{subName}/index.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    return dataset


def scrape_comments(data):
    print(f'Fetching posts... \n')
    for post in data:
        # Fetch comments
        # print(f'Fetching post {post["id"]}... \n')
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
        "https://www.reddit.com/r/stocks/.json",
        params={"limit": "5"}
    )
    
    json_data = response.json()
    
    if response.status_code != 200:
        raise Exception("Failed to fetch!")
    
    with open(f"test.json", "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)

def main():
    scraper()
    # test()


main()
