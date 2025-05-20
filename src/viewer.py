import argparse
import glob
import json
import os
from collections import Counter
from typing import Literal

import cv2
import numpy as np
import pandas as pd
import requests

from constant import SELECTED_DATA_DIR
from visualize import make_histogram


def load_and_summarize(
    json_path, sort_col: Literal["likeScore", "createdAt"] = "likeScore"
):
    items = []
    if os.path.isdir(json_path):
        # Iterate all JSON files in the directory
        for file in glob.glob(os.path.join(json_path, "civitai_datas_*.json")):
            with open(file, encoding="utf-8") as f:
                data = json.load(f)
                items.extend(data.get("items", []))
    else:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
            items = data.get("items", [])

    df = pd.DataFrame(items)

    def calc_custom_score(stats):
        if not isinstance(stats, dict):
            return 0
        return (
            stats.get("likeCount", 0)
            + stats.get("cryCount", 0)
            + stats.get("laughCount", 0)
            + stats.get("heartCount", 0)
            - stats.get("dislikeCount", 0)
        )

    df["likeScore"] = df["stats"].apply(calc_custom_score)

    nsfw_summary = df["nsfwLevel"].value_counts().to_dict()
    base_model_summary = df["baseModel"].value_counts(dropna=True).to_dict()

    def summarize_resources(col):
        resources = []
        for meta in df["meta"].dropna():
            for res in meta.get(col, []):
                resources.append(res.get("type", "unknown"))
        return dict(Counter(resources))

    resources_summary = summarize_resources("resources")
    civitai_resources_summary = summarize_resources("civitaiResources")

    df = df.sort_values(sort_col, ascending=False).reset_index(drop=True)
    return {
        "df": df,
        "nsfw_summary": nsfw_summary,
        "base_model_summary": base_model_summary,
        "resources_summary": resources_summary,
        "civitai_resources_summary": civitai_resources_summary,
    }


def url_to_image(url):
    try:
        resp = requests.get(url, timeout=10)
        arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Image decode error")
        return img
    except Exception as e:
        img = np.ones((300, 300, 3), dtype=np.uint8) * 128
        cv2.putText(
            img, str(e), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1
        )
        return img

def draw_summary(img, info_lines, limit_height=2400):
    h, w = img.shape[:2]
    new_h = limit_height
    new_w = int(w * (new_h / h))
    img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    h, w = img.shape[:2]

    panel = np.ones((300, w, 3), dtype=np.uint8) * 240
    for i, line in enumerate(info_lines):
        cv2.putText(
            panel, line, (10, 30 + 30 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2
        )
    return np.vstack([img, panel])


def show_images_with_summary(df):
    idx = 0
    total = len(df)

    def get_image_url(row):
        return row["url"]

    def get_image_info(row):
        return [
            f"Index: {idx+1}/{total}",
            f"ID: {row['id']}",
            f"NSFW: {row.get('nsfwLevel', '-')}",
            f"Like: {row.get('likeScore', 0)}",
            f"Base model: {row.get('baseModel', 'N/A')}",
            f"Resources: {len(row.get('resources', []))}",
            f"Civitai resources: {len(row.get('meta', {}).get('civitaiResources', [])) if isinstance(row.get('meta', {}), dict) else 0}",
            f"pp: {row.get('meta', {}).get('prompt', '')[:100] if row.get('meta', {}) is not None else 'N/A'}",
            f"nn: {row.get('meta', {}).get('negativePrompt', '')[:100] if row.get('meta', {}) is not None else 'N/A'}",
        ]

    while True:
        try:
            row = df.iloc[idx]
            img_url = get_image_url(row)
            img = url_to_image(img_url)
            info = get_image_info(row)
            img_with_panel = draw_summary(img, info)
            cv2.imshow(
                "Civitai Image Viewer (q: prev, a: next, d: save, p: quit)",
                img_with_panel,
            )
            key = cv2.waitKey(0)
            if key == ord("p"):
                break
            elif key == ord("a"):  # skip
                idx = min(idx + 1, total - 1)
            elif key == ord("q"):  # prev
                idx = max(idx - 1, 0)
            elif key == ord("d"):  # save
                selected_data = df.iloc[idx].to_dict()
                selected_json_path = f"{SELECTED_DATA_DIR}/selected_datas.json"

                try:
                    with open(selected_json_path, "r", encoding="utf-8") as f:
                        selected_json = json.load(f)
                    if "items" not in selected_json or not isinstance(
                        selected_json["items"], list
                    ):
                        selected_json["items"] = []
                except (FileNotFoundError, json.JSONDecodeError):
                    selected_json = {"items": []}

                selected_json["items"].append(selected_data)
                with open(selected_json_path, "w", encoding="utf-8") as f:
                    json.dump(selected_json, f, indent=4, ensure_ascii=False)
                idx = min(idx + 1, total - 1)

        except Exception as e:
            print(f"ID {row['id']}: {e}")
            key = cv2.waitKey(0)
            if key == ord("a"):  # skip
                idx = min(idx + 1, total - 1)
            elif key == ord("q"):  # prev
                idx = max(idx - 1, 0)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("datas", type=str, help="Folder path to save crawled data")
    parser.add_argument(
        "--sort-col",
        type=str,
        default="likeScore",
        choices=["likeScore", "createdAt"],
        help="Column to sort by",
    )
    args = parser.parse_args()

    summary = load_and_summarize(args.datas, args.sort_col)
    print(summary["df"], "\n---------")
    print(f"[NSFW 분포]: \n{summary['nsfw_summary']}\n---------")
    print(f"[BaseModel 분포]: \n{summary['base_model_summary']}\n---------")
    print(f"[Resources 분포]: \n{summary['resources_summary']}\n---------")
    print(f"[CivitaiResources 분포]: \n{summary['civitai_resources_summary']}\n---------")
    
    print("[LikeScore histogram]")
    make_histogram(summary["df"], "likeScore", bins=20, width=100)

    print("[Image viewer]\n")
    show_images_with_summary(summary["df"])
