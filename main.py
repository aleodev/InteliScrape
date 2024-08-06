import time
import httpx
import pandas as pd


def grabber():
    # Retrieval point for any subreddit
    base_url = "https://www.reddit.com"
    endpoint = "/r/stocks"
    category = "/hot"

    url = base_url + endpoint + category + ".json"
    after_post_id = None

    dataset = []

    # Capped at last 500 posts for now
    # Should probably make scheduler
    for _ in range(5):
        params = {"limit": 100, "t": "year", "after": after_post_id}  # time units
        response = httpx.get(url, params=params)

        print(f'fetching"{response.url}"...')
        if response.status_code != 200:
            raise Exception("Failed to fetch!")

        json_data = response.json()

        dataset.extend([rec["data"] for rec in json_data["data"]["children"]])

        after_post_id = json_data["data"]["after"]
        time.sleep(0.5)

    df = pd.DataFrame(dataset)
    df.to_csv("export/reddit_python.csv", index=True)


def main():
    grabber()


main()
