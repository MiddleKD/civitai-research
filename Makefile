.PHONY: crawl show_json_types view format count_selected analyze_json

crawl:
	uv run src/crawl_civitai.py --limit 100 --depth 1000 --nsfw

show_json_types:
	uv run src/show_json_types.py ./datas/sample.json --max-depth 4

view:
	uv run src/viewer.py datas

format:
	black src
	isort src

count_selected:
	jq '.items | length' datas/selected/selected_datas.json 

analyze_json:
	uv run src/analyze_json.py --json-path ./datas/selected/250516_selected_datas.json