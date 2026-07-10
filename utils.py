import csv
import json
from pathlib import Path

def list_word_files():
    return sorted([f.name for f in Path(".").glob("words*.csv")])

def load_words(csv_file):
    words = []
    for encoding in ["utf-8-sig", "utf-8"]:
        try:
            with open(csv_file, newline='', encoding=encoding) as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 3:
                        words.append({
                            "char": row[0].strip(),
                            "pinyin": row[1].strip(),
                            "english": row[2].strip()
                        })
            break
        except UnicodeDecodeError:
            continue
    return words

def load_ratings(filename):
    path = Path(filename)
    if not path.exists() or path.stat().st_size == 0:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_ratings(filename, ratings):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(ratings, f, ensure_ascii=False, indent=2)
