import json
from collections import Counter
import pandas as pd
from visualize import make_histogram

from typing import Dict
import json
from collections import Counter
import pandas as pd
from visualize import make_histogram

def print_menu(options: list[str]) -> int:
    print("\n=== DataFrame 선택 ===")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    print(f"{len(options)+1}. 종료(exit)")
    while True:
        sel = input("번호를 선택하세요: ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(options)+1:
            return int(sel)
        print("잘못된 입력입니다. 다시 선택하세요.")

def get_count_filter() -> int | None:
    while True:
        val = input("몇 개 이상의 count만 출력할까요? (정수 입력, 엔터 시 전체): ").strip()
        if val == '':
            return None
        if val.isdigit():
            return int(val)
        print("잘못된 입력입니다. 다시 입력하세요.")

def interact_with_df(df_dict: Dict[str, pd.DataFrame], counter_dict: Dict[str, Counter]):
    options = list(df_dict.keys())
    while True:
        sel = print_menu(options)
        if sel == len(options)+1:
            print("프로그램을 종료합니다.")
            break
        prefix = options[sel-1]
        df = df_dict[prefix]
        counter = counter_dict[prefix]
        print(f"\n--- {prefix} 빈도 Counter ---")
        print(counter)
        print(f"\n--- {prefix} DataFrame 미리보기 ---")
        print(df.head())
        make_histogram(df, "count", bins=20, width=100)
        count_filter = get_count_filter()
        if count_filter is not None:
            filtered = df[df['count'] >= count_filter]
        else:
            filtered = df
        print(f"\n[{prefix}] count >= {count_filter if count_filter is not None else '전체'} 결과:")
        print(filtered)
        print("\n출력이 끝났습니다. 다시 DataFrame을 선택하세요.")

def main(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 빈도 집계용 Counter
    model_name_counter = Counter()
    resources_counter = Counter()
    civitai_resources_counter = Counter()
    additional_resources_counter = Counter()

    for item in data.get('items', []):
        meta = item.get('meta') or {}

        # base model name
        base_model = item.get('baseModel')
        if base_model:
            model_name_counter[base_model] += 1

        # resources
        resources = meta.get('resources')
        if resources:
            for resource in resources:
                resources_counter[resource.get("name")] += 1

        # civitai resources
        civitai_resources = meta.get('civitaiResources')
        if civitai_resources:
            for resource in civitai_resources:
                civitai_resources_counter[resource.get("modelVersionId")] += 1

        # additional resources
        additional_resources = meta.get('additionalResources')
        if additional_resources:
            for resource in additional_resources:
                additional_resources_counter[resource.get("name")] += 1

    # DataFrame 생성 및 prefix dict에 저장
    dfs = {
        "base_model": pd.DataFrame(model_name_counter.items(), columns=['model_name', 'count']),
        "resources": pd.DataFrame(resources_counter.items(), columns=['resource', 'count']),
        "civitai_resources": pd.DataFrame(civitai_resources_counter.items(), columns=['civitai_resource', 'count']),
        "additional_resources": pd.DataFrame(additional_resources_counter.items(), columns=['additional_resource', 'count'])
    }
    counters = {
        "base_model": model_name_counter,
        "resources": resources_counter,
        "civitai_resources": civitai_resources_counter,
        "additional_resources": additional_resources_counter
    }
    interact_with_df(dfs, counters)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Analyze Civitai JSON file and interact with DataFrames.")
    parser.add_argument(
        "--json-path",
        type=str,
        default="./datas/selected/selected_datas.json",
        help="분석할 JSON 파일 경로 (기본값: ./datas/selected/selected_datas.json)",
    )
    args = parser.parse_args()
    main(args.json_path)
