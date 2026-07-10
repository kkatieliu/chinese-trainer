# Chinese Vocabulary Trainer 中文单词训练器

A command-line flashcard app for studying HSK Chinese vocabulary (HSK 3–5),
with self-rated difficulty tracking and adaptive study sessions.

## Features

- **Flashcard sessions** — see a character, reveal its pinyin and English, rate yourself 1–5
- **Adaptive session pool** — words rated 1⭐ stay in the current session until you improve; words rated 2–5⭐ are cleared from the session
- **Persistent progress** — ratings are saved to `ratings.json` after every answer, so you can quit anytime without losing progress
- **Grouped study** — vocabulary is split into groups of 20 words; study any combination (`1,3,5` or ranges like `1-4`)
- **Rating filters** — review only the words you rated a specific score (e.g. drill just your 1⭐ words)
- **Progress dashboard** — see a per-group breakdown of your ratings every time you return to the menu

## Demo
=== Chinese Vocabulary Trainer ===
Group 1 (words1.csv): 1⭐=4, 2⭐=3, 3⭐=6, 4⭐=2, 5⭐=5 (total 20)
Which groups do you want to study? (e.g. 1,2,3 or 1-3 or q to quit): 1
Character: 安静
Press Enter to reveal, or type 'next' to exit:
→ ānjìng = quiet
Rate 1–5 (5 = best): 4
Updated 安静 → 4⭐, removed from session.

## Getting Started

Requires Python 3.8+. No external dependencies.

```bash
git clone https://github.com/kkatieliu/chinese-trainer.git
cd chinese-trainer
python3 main.py
```

## Project Structure

| File | Purpose |
|------|---------|
| `main.py` | CLI menu: group selection, rating filters, session loop |
| `trainer.py` | Core logic: group building, summaries, adaptive study sessions |
| `utils.py` | CSV/JSON loading and saving |
| `*.csv` | HSK 3–5 vocabulary lists (character, pinyin, English) |
| `ratings.json` | Auto-generated file storing your per-word ratings |

## How Ratings Work

Each word starts at 1⭐. During a session:
- **Rating 1** → the word stays in the session pool for more practice
- **Ratings 2–5** → the word is removed from the current session

Ratings persist between sessions, so over time the dashboard shows your
progress across the full HSK 3–5 vocabulary.

## Roadmap

- Spaced-repetition scheduling based on rating history
- Audio playback for pronunciation
- Reverse mode (English → character recall)