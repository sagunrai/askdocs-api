"""Download Wikipedia pages as plain text. Text is CC BY-SA 4.0 from Wikipedia."""

import os
import requests

PAGES = [
    "Nepal",
    "Kathmandu",
    "Mount Everest",
    "History of Nepal",
    "Culture of Nepal",
    "Himalayas",
    "Pokhara",
    "Lumbini",
    "Nepalese cuisine",
    "Economy of Nepal",
    "Languages of Nepal",
    "April 2015 Nepal earthquake",
    "Tourism in Nepal",
    "Kathmandu Valley",
    "Sherpa people",
]

URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "askdocs-api/1.0 (https://github.com/yourusername/askdocs-api)"}
PARAMS = {
    "action": "query",
    "prop": "extracts",
    "explaintext": "1",
    "format": "json",
    "exsectionformat": "plain",
}

DATA_DIR = os.getenv("DATA_DIR", "data")
os.makedirs(DATA_DIR, exist_ok=True)


def sanitize_filename(title: str) -> str:
    return title.lower().replace(" ", "_") + ".txt"


def main():
    for title in PAGES:
        params = PARAMS.copy()
        params["titles"] = title
        try:
            resp = requests.get(URL, params=params, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            pages = data.get("query", {}).get("pages", {})
            page = next(iter(pages.values()))
            text = page.get("extract", "")
            if not text:
                print(f"[skip] {title}: empty extract")
                continue
            text = text[:30000]
            filename = sanitize_filename(title)
            path = os.path.join(DATA_DIR, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"[ok] {filename}: {len(text)} chars")
        except Exception as e:
            print(f"[error] {title}: {e}")


if __name__ == "__main__":
    main()