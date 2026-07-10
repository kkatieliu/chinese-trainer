import random
from utils import load_words, load_ratings, save_ratings, list_word_files

GROUP_SIZE = 20

class Trainer:
    def __init__(self, ratings_file):
        self.ratings_file = ratings_file
        self.ratings = load_ratings(ratings_file)
        self.word_files = list_word_files()
        self.groups = self._build_groups()

    def _build_groups(self):
        groups = []
        for file in self.word_files:
            words = load_words(file)
            for i in range(0, len(words), GROUP_SIZE):
                chunk = words[i:i+GROUP_SIZE]
                groups.append({"file": file, "words": chunk})
        return groups

    def get_group_summary(self, group):
        file = group["file"]
        words = group["words"]
        group_ratings = self.ratings.get(file, {})

        counts = {1:0, 2:0, 3:0, 4:0, 5:0}
        for w in words:
            r = group_ratings.get(w["char"], 1)
            # make sure r is valid
            if r not in counts:
                r = 1
            counts[r] += 1
        return counts


    def show_overall_summary(self):
        print("Your current progress:\n")
        for idx, group in enumerate(self.groups, start=1):
            stats = self.get_group_summary(group)
            total = sum(v for k, v in stats.items() if isinstance(v, int))
            print(f"Group {idx} ({group['file']}): " + 
                ", ".join(f"{k}⭐={v}" for k, v in stats.items()) +
                f" (total {total})")
    
    def study(self, group_ids, filter_rating=None):
        # --- Combine all selected groups into one pool ---
        all_selected_words = []
        for gid in group_ids:
            if gid < 1 or gid > len(self.groups):
                print(f"Invalid group {gid}")
                continue

            group = self.groups[gid - 1]
            file = group["file"]
            words = group["words"]

            print(f"=== Group {gid} Summary ({file}) ===")
            stats = self.get_group_summary(group)
            print(", ".join(f"{k}⭐={v}" for k, v in stats.items()) + "\n")

            # Add (file, word) pairs so we know where each came from
            all_selected_words.extend([(file, w) for w in words])

        if not all_selected_words:
            print("No valid groups selected.")
            return

        # --- Build weighted pool across all groups combined ---
        selected = []
        for file, w in all_selected_words:
            group_ratings = self.ratings.get(file, {})
            r = group_ratings.get(w["char"], 1)
            if filter_rating is not None and r != filter_rating:
                continue
            # No weighting: each word appears exactly once in the session pool.
            selected.append((file, w))

        if not selected:
            print("No words match this filter.")
            return

        random.shuffle(selected)
        total_entries = len(selected)
        print(f"\n=== Studying Combined Groups {', '.join(map(str, group_ids))} ===")
        print(f"Starting session with {total_entries} words.\n")

            # --- Study loop (manual index for safe mutation) ---
        i = 0
        while i < len(selected):
            file, w = selected[i]
            print(f"Character: {w['char']}  ({file})")
            cmd = input("Press Enter to reveal, or type 'next' to exit: ").strip().lower()
            if cmd in ["next", "n"]:
                print("\nReturning to main menu...\n")
                return

            print(f" → {w['pinyin']} = {w['english']}\n")

            # Get rating safely
            while True:
                try:
                    r = int(input("Rate 1–5 (5 = best): "))
                    if 1 <= r <= 5:
                        break
                except ValueError:
                    pass
                print("Please enter a number 1–5.")

            # Save rating
            if file not in self.ratings:
                self.ratings[file] = {}
            self.ratings[file][w["char"]] = r
            save_ratings(self.ratings_file, self.ratings)

            # --- Dynamically adjust pool based on rating ---
            # New behavior: only rating 1 keeps the word in the current session (possibly with duplicates).
            # Any other rating (2,3,4,5) removes the word completely from the session pool.
            if r == 1:
                unique_remaining = len(set(x["char"] for _, x in selected))
                total_remaining = len(selected)
                print(f"Updated {w['char']} → 1⭐. Kept in session. Pool now has {total_remaining} entries ({unique_remaining} unique words).\n")
                i += 1  # move to next item
                continue

            else:
                # Remove all copies for ratings 2–5
                selected = [(f, x) for f, x in selected if x["char"] != w["char"]]
                unique_remaining = len(set(x["char"] for _, x in selected))
                total_remaining = len(selected)
                print(f"Updated {w['char']} → {r}⭐, removed from session. Pool now has {total_remaining} entries ({unique_remaining} unique words).\n")
                # do not increment i; next loop iteration will process the item now at index i
                continue

        print("\nAll selected groups complete! Returning to menu.\n")



   