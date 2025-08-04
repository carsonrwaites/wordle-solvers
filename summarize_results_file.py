# summarize_results_file.py
import json
from collections import Counter

def summarize_results_from_file(filename):
    # Load JSON file
    with open(filename, "r", encoding="utf-8") as f:
        games = json.load(f)

    # Analyze results
    solve_lengths = Counter()
    guess_frequency = Counter()

    for game in games:
        if game["result"] == "win":
            solve_lengths[len(game["guesses"])] += 1
        else:
            solve_lengths["X"] += 1
        guess_frequency.update(game["guesses"])

    # Print summary
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
    # Example usage
    filename = "results/minimax_arise_results.txt"
    summarize_results_from_file(filename)

