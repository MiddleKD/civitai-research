import argparse
import json
import logging
import os

import requests

from constant import CIVITAI_URL, DATA_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CursorNotFoundException(Exception):
    pass


def save_json(data: dict, fn: str):
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def crawl_images(cursor: str, params: dict) -> str:
    """
    Args:
        cursor (str): If not None, then fetch image data from the next cursor.
        params (dict): Parameters to be passed to the API.

    Returns:
        str: The last cursor of the fetched data.
    """
    logger.info(f"Requesting with cursor {cursor} and params {params} ...")

    resp = requests.get(CIVITAI_URL, params={"cursor": cursor, **params})
    if resp.status_code != 200:
        raise requests.HTTPError(f"Error: HTTP {resp.status_code}")

    data = resp.json()

    save_json(data, os.path.join(DATA_DIR, f"civitai_datas_{cursor}.json"))
    count = len(data.get("items", []))
    logger.info(f"Fetched {count} images. Saved result to {cursor}")

    cursor = data.get("metadata", {}).get("nextCursor")

    if not cursor:
        raise CursorNotFoundException("No more cursor. Done.")

    return cursor.split("|")[0]


def run(limit: int, nsfw: bool, depth: int):
    params = {"limit": limit, "nsfw": "true" if nsfw else "false"}

    cursor = None
    for _ in range(depth):
        try:
            cursor = crawl_images(cursor, params)
        except requests.HTTPError as e:
            logger.error(f"Error: {e}")
        except CursorNotFoundException as e:
            logger.info(f"Cursor not found is crawl done.")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--limit", type=int, default=100, help="Limit of images to fetch"
    )
    parser.add_argument(
        "-d", "--depth", type=int, default=5, help="Maximum cursor depth to crawl"
    )
    parser.add_argument("-n", "--nsfw", action="store_true", help="Include NSFW images")
    args = parser.parse_args()

    run(args.limit, args.nsfw, args.depth)
