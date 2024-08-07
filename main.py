import time
import httpx
import json
from constants import subreddits


def scrapper():
    # Capped at last 500 posts per sub for now
    # Anything past 3 times per 100, the 4th is blank for some reason???
    # Should probably make scheduler

    for sub in subreddits:
        print(f"Fetching ${sub} \n")

        # Scrape posts
        dataset = scrape_posts(sub)

        # Scrape comments using posts url
        updated_dataset = scrape_comments(dataset)


def scrape_posts(subName):
    postLimit = 100
    postRate = 1
    # Data
    data = []
    # Grab chunk past ID
    after_post_id = None

    # Retrieval point for any subreddit
    category = "hot"
    url = f"https://www.reddit.com/r/{subName}/{category}.json"

    for _ in range(postRate):
        params = {"limit": postLimit, "t": "year", "after": after_post_id}  # time units
        response = httpx.get(url, params=params)

        print(f'Fetching chunk {_} "{response.url}"... \n')

        if response.status_code != 200:
            raise Exception("Failed to fetch!")

        json_data = response.json()

        parsed = [rec["data"] for rec in json_data["data"]["children"]]
        keys = ["id", "title", "url"]
        filtered = [{key: item[key] for key in keys} for item in parsed]

        data.extend(filtered)

        # Set ID to grab next chunk
        after_post_id = json_data["data"]["after"]
        time.sleep(0.5)
    return data


def scrape_comments(data):
    print(data)
    for post in data:
        response = httpx.get(f'{post["url"]}.json')

        if response.status_code != 200:
            raise Exception("Failed to fetch!")

        json_data = response.json()

        parsed = json_data[1]

        with open(f"export/{post["id"]}.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=4, ensure_ascii=False)


def flatten_comments(data):
    comments = []

    def recurse(item):
        if isinstance(item, dict) and "data" in item:
            data_item = item["data"]
            if "body" in data_item:
                comments.append(data_item["body"])
            if "replies" in data_item and "children" in data_item["replies"]:
                for child in data_item["replies"]["children"]:
                    recurse(child)

    for entry in data:
        recurse(entry)

    return comments

def flatten_comments(data):
    bodies = []
    
    def traverse(item):
        if isinstance(item, dict):
            # Check if 'data' key is present
            if 'data' in item:
                data = item['data']
                
                # Check if 'body' key is present and add to bodies list
                if 'body' in data:
                    bodies.append(data['body'])
                
                # Recursively traverse 'replies'
                if 'replies' in data and isinstance(data['replies'], dict):
                    children = data['replies'].get('data', {}).get('children', [])
                    for child in children:
                        traverse(child)
    
    # Traverse each item in the list
    for item in data:
        traverse(item)
        
    
    return bodies

def group_comments(comments):
    def process_comment(comment):
        result = {}
        if "body" in comment["data"]:
            result["comment"] = comment["data"]["body"]
        if "replies" in comment["data"] and comment["data"]["replies"]:
            replies = comment["data"]["replies"]
            if isinstance(replies, dict) and "data" in replies and "children" in replies["data"]:
                result["replies"] = process_comments(replies["data"]["children"])
        return result

    def process_comments(comments):
        return [process_comment(comment) for comment in comments]

    return process_comments(comments)


def test():
    
    response = httpx.get(
        "https://www.reddit.com/r/stocks/comments/1d5itn0/rate_my_portfolio_rstocks_quarterly_thread_june/.json"
    )

    if response.status_code != 200:
        raise Exception("Failed to fetch!")
    
    json_data = response.json()
    parsed_data = json_data[1]["data"]["children"]
    
    flat_data = list(flatten_comments(parsed_data))
    group_data = list(group_comments(parsed_data))


    with open(f"export/parsed_comments.json", "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=4, ensure_ascii=False)
        
    with open(f"export/grouped_comments.json", "w", encoding="utf-8") as f:
        json.dump(group_data, f, indent=4, ensure_ascii=False)
        
    with open(f"export/flattened_comments.json", "w", encoding="utf-8") as f:
        json.dump(flat_data, f, indent=4, ensure_ascii=False)


def main():
    test()


main()
