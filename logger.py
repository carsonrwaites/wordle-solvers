from collections import Counter
import json

class Logger:
    def __init__(self):
        self.games = []

    def log_game(self, result):
        """
        result is expected to be:
        {
            'answer': str,
            'guesses': [str],
            'result': 'win' or 'loss'
        }
        """
        self.games.append(result)

    def summarize(self):
        solve_lengths = Counter()
        guess_frequency = Counter()

        for game in self.games:
            if game["result"] == "win":
                solve_lengths[len(game["guesses"])] += 1
            else:
                solve_lengths["X"] += 1  # did not solve

            guess_frequency.update(game["guesses"])

        return {
            "total_games": len(self.games),
            "solve_lengths": dict(solve_lengths),
            "guess_frequency": dict(guess_frequency)
        }

    def print_summary(self):
        summary = self.summarize()
        print("\n--- Results Summary ---")
        print(f"Total games: {summary['total_games']}")
        print("Solve lengths:")
        for length, count in summary["solve_lengths"].items():
            print(f"  {length}: {count}")
        print("\nTop 10 guessed words:")
        for word, count in sorted(summary["guess_frequency"].items(), key=lambda x: -x[1])[:10]:
            print(f"{word}: {count}")

    def dump_results_to_file(self, filename="results.txt"):
        """
        Dump all game results to a text file as JSON.
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.games, f, indent=4)
        print(f"Results dumped to {filename}")