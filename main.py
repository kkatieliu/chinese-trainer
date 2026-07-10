from trainer import Trainer

def main():
    print("=== Chinese Vocabulary Trainer ===\n")
    print("loading trainer...")

    trainer = Trainer("ratings.json")
    print("trainer loaded!") 

    while True:
        # ---- Always show the current summaries before choosing ----
        print("\nCurrent progress:\n")
        trainer.show_overall_summary()

        # ---- Group Selection ----
        groups_input = input("\nWhich groups do you want to study? (e.g. 1,2,3 or 1-3 or q to quit): ").strip()
        if groups_input.lower() in ("q", "quit", "exit"):
            print("\nGoodbye! Progress saved.")
            break

        def parse_group_list(s):
            ids = set()
            for part in s.split(','):
                part = part.strip()
                if not part:
                    continue
                # range like 1-5
                if '-' in part:
                    bounds = part.split('-')
                    if len(bounds) == 2 and bounds[0].strip().isdigit() and bounds[1].strip().isdigit():
                        a = int(bounds[0].strip())
                        b = int(bounds[1].strip())
                        if a <= b:
                            ids.update(range(a, b+1))
                        else:
                            ids.update(range(b, a+1))
                    else:
                        # ignore malformed part
                        continue
                elif part.isdigit():
                    ids.add(int(part))
                else:
                    # ignore non-numeric parts
                    continue
            return sorted(ids)

        group_ids = parse_group_list(groups_input)
        if not group_ids:
            print("Please enter at least one group number (supports ranges like 1-3).")
            continue

        # ---- Rating Filter ----
        filter_rating = input("Filter by rating (1–5 or leave blank for all): ").strip()

        if filter_rating.lower() in ("q", "quit", "exit"):
            print("\nReturning to main menu...\n")
            continue

        if filter_rating.isdigit():
            filter_rating = int(filter_rating)
        else:
            filter_rating = None

        # ---- Study Session ----
        trainer.study(group_ids, filter_rating)

        # ---- Automatically return to menu and refresh summary ----
        print("\nReturning to main menu...\n")

if __name__ == "__main__":
    main()
