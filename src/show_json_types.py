import argparse
import json


def print_types(obj, prefix="", depth=1, max_depth=2):
    if isinstance(obj, dict):
        for k, v in obj.items():
            print(f"{prefix}{k}: {type(v).__name__}")
            if isinstance(v, (dict, list)) and depth < max_depth:
                print_types(v, prefix + "  ", depth + 1, max_depth)
    elif isinstance(obj, list) and obj:
        print(f"{prefix}[list of {type(obj[0]).__name__}]")
        if isinstance(obj[0], (dict, list)) and depth < max_depth:
            print_types(obj[0], prefix + "  ", depth + 1, max_depth)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Show JSON key and value types.")
    parser.add_argument("json_file", help="Path to the JSON file")
    parser.add_argument(
        "--max-depth",
        "-d",
        type=int,
        default=2,
        help="Maximum depth to display (default: 2)",
    )
    args = parser.parse_args()

    with open(args.json_file, encoding="utf-8") as f:
        data = json.load(f)
    print_types(data, max_depth=args.max_depth)
