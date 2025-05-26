# Civitai Research

Civitai Image Crawling and Data Insight Analysis Project

---

## Project Overview

This project is a data research tool that crawls images from the AI image sharing website [Civitai](https://civitai.com/), collects and analyzes their metadata, and provides insights into AI image generation trends and model usage statistics.

- **Automated image and metadata collection**
- **Selection of interesting images and statistical analysis**
- **Civitai API integration and automation**

---

## Main Features

| Feature             | Description                                                                                   |
|---------------------|---------------------------------------------------------------------------------------------|
| `crawl`             | Crawl images and metadata from Civitai, save as JSON                                         |
| `show_json_types`   | Check the key-value structure and types of the crawled JSON files                             |
| `view`              | Browse images and metadata, select interesting images, save selected images in datas/selected |
| `count_selected`    | Count the number of selected images (data)                                                   |
| `analyze_json`      | Analyze metadata of selected images, provide statistics such as used models                  |

---

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository URL>
   cd civitai-research
   ```

2. **Prepare Python 3.10+ environment**

3. **Install dependencies**
   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   ```

4. **Create .env file and register API Key**
   ```env
   CIVITAI_API_KEY=your_api_key_here
   ```
   - You can get your API Key from [Civitai](https://civitai.com/).

---

## Usage

### 1. Crawl Images
```bash
make crawl
```
- Runs `src/crawl_civitai.py`
- Crawls images and metadata from Civitai, saves as civitai_datas_*.json in the datas/ folder

### 2. Check JSON Structure
```bash
make show_json_types
```
- Checks the key-value type structure of the crawled JSON files

### 3. Image Viewer & Select Interesting Images
```bash
make view
```
- Browse images and metadata, select images of interest
- Selected images are saved as JSON files in datas/selected/

### 4. Count Selected Images
```bash
make count_selected
```
- Outputs the number of selected images (data)

### 5. Analyze Selected Image Data
```bash
make analyze_json
```
- Analyzes the metadata of selected images, provides insights such as statistics on used AI models

---

## Folder Structure

```
civitai-research/
├── datas/                 # Folder for crawled and selected data
│   └── selected/          # Folder for selected image data
├── src/                   # Main Python source code
│   ├── crawl_civitai.py   # Civitai image crawler
│   ├── show_json_types.py # JSON structure/type checker
│   ├── viewer.py          # Image viewer and selection tool
│   ├── analyze_json.py    # Selected image data analyzer
│   ├── visualize.py       # Visualization functions
│   └── constant.py        # Constants and path definitions
├── pyproject.toml         # Python project settings and dependencies
├── Makefile               # Main command shortcuts
├── .env                   # Environment variable file (must be created manually)
└── README.md              # Project description file
```

---

## Example Workflow

1. **Crawling**: `make crawl` → Creates civitai_datas_*.json in datas/
2. **Check Structure**: `make show_json_types` → Understand JSON structure
3. **Select Images**: `make view` → Save interesting images in datas/selected/
4. **Count**: `make count_selected` → Count the number of selected data
5. **Analysis**: `make analyze_json` → Analyze statistics of models/parameters used in selected images

---

This project was created for research purposes to analyze and gain insights from data on the open-source AI image platform [Civitai](https://civitai.com/).