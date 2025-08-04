import json
from collections import Counter

# Results from runs should be in a subfolder called 'results'

def summarize_results_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        games = json.load(f)

    solve_lengths = Counter()
    guess_frequency = Counter()

    for game in games:
        if game["result"] == "win":
            solve_lengths[len(game["guesses"])] += 1
        else:
            solve_lengths["X"] += 1
        guess_frequency.update(game["guesses"])

    print(f"--- Summary for {filename} ---")
    print(f"Total games: {len(games)}")
    print("Solve lengths:")
    for length, count in solve_lengths.items():
        print(f"  {length}: {count}")
    print("\nTop 10 guessed words:")
    for word, count in sorted(guess_frequency.items(), key=lambda x: -x[1])[:10]:
        print(f"{word}: {count}")
    print()

if __name__ == "__main__":
    filename = "results/minimax_arise_results.txt"
    summarize_results_from_file(filename)
