import configparser
import os
from definitions import CONFIG_PATH


def flatten_comments(data):
    dataset = []

    def traverse(item):
        if isinstance(item, dict):
            # Check if 'data' key is present
            if "data" in item:
                data = item["data"]

                # Check if 'body' key is present and add to comments list
                if "body" in data:
                    dataset.append(data["body"])

                # Recursively traverse 'replies'
                if "replies" in data and isinstance(data["replies"], dict):
                    children = data["replies"].get("data", {}).get("children", [])
                    for child in children:
                        traverse(child)

    # Traverse each item in the list
    for item in data:
        traverse(item)

    return dataset


def group_comments(comments):
    def process_comment(comment):
        result = {}
        if "body" in comment["data"]:
            result["comment"] = comment["data"]["body"]
        if "replies" in comment["data"] and comment["data"]["replies"]:
            replies = comment["data"]["replies"]
            if (
                isinstance(replies, dict)
                and "data" in replies
                and "children" in replies["data"]
            ):
                result["replies"] = process_comments(replies["data"]["children"])
        return result

    def process_comments(comments):
        return [process_comment(comment) for comment in comments]

    return process_comments(comments)


def setup_config(section, default_config):
    # Setup config
    config = configparser.ConfigParser()

    # Config doesnt exist
    if not os.path.exists(CONFIG_PATH):
        config[section] = default_config
        with open(CONFIG_PATH, "w") as f:
            config.write(f)

    else:
        config.read(CONFIG_PATH)
        # Config exists without section
        if not config.has_section(section):
            config.add_section(section)
            for key, value in default_config.items():
                config.set(section, key, value)
            with open(CONFIG_PATH, "w") as f:
                config.write(f)
