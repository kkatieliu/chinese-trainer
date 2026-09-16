import csv
import json
import re
from pathlib import Path

def list_word_files():
    return sorted([f.name for f in Path(".").glob("words*.csv")])

def load_words(csv_file):
    words = []
    for encoding in ["utf-8-sig", "utf-8"]:
        try:
            with open(csv_file, newline='', encoding=encoding) as f:
                reader = csv.reader(f)
                def contains_chinese(s):
                    if not s:
                        return False
                    return bool(re.search(r"[\u4e00-\u9fff]", s))

                for row in reader:
                    # normalize: strip each cell
                    row = [c.strip() for c in row if c is not None]
                    if not row:
                        continue

                    # Combine any trailing columns as english definition
                    english = ""

                    source_order = "char-first"
                    if len(row) >= 3:
                        # If any cell contains Chinese characters, prefer that as `char`.
                        if contains_chinese(row[0]):
                            char = row[0]
                            pinyin = row[1] if len(row) > 1 else ""
                            english = ", ".join(row[2:]) if len(row) > 2 else ""
                            source_order = "char-first"
                        elif contains_chinese(row[1]):
                            # maybe pinyin then char then english
                            char = row[1]
                            pinyin = row[0]
                            english = ", ".join(row[2:]) if len(row) > 2 else ""
                            source_order = "pinyin-first"
                        else:
                            # Fallback: assume char, pinyin, english
                            char = row[0]
                            pinyin = row[1]
                            english = ", ".join(row[2:])
                            source_order = "char-first"

                    elif len(row) == 2:
                        # Two-column format: either (char, pinyin) or (pinyin, char)
                        a, b = row[0], row[1]
                        if contains_chinese(a) and not contains_chinese(b):
                            char = a
                            pinyin = b
                            source_order = "char-first"
                        elif contains_chinese(b) and not contains_chinese(a):
                            char = b
                            pinyin = a
                            source_order = "pinyin-first"
                        else:
                            # Neither contains obvious Chinese characters; assume pinyin, char
                            char = b
                            pinyin = a
                            source_order = "pinyin-first"

                    else:
                        # single-column or unexpected format — skip
                        continue

                    words.append({
                        "char": char.strip(),
                        "pinyin": pinyin.strip(),
                        "english": english.strip(),
                        "source_order": source_order
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
