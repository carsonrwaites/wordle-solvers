import csv
import math
from collections import defaultdict


class WordleSolver:
    def __init__(self, word_file):
        self.all_guesses = self.load_words(word_file)
        self.possible_answers = self.all_guesses.copy()

    def load_words(self, filename):
        # CSV file, one word per line, utf-8-sig encoding
        with open(filename, 'r', encoding='utf-8-sig') as f:
            return [line.strip() for line in f if line.strip()]

    def get_feedback_pattern(self, guess, answer):
        """
        Returns a feedback pattern string (length 5) of:
        G = Green, Y = Yellow, B = Black/Gray
        """
        result = ['B'] * 5
        answer_chars = list(answer)

        # Green pass
        for i, (g, a) in enumerate(zip(guess, answer)):
            if g == a:
                result[i] = 'G'
                answer_chars[i] = None

        # Yellow pass
        for i, g in enumerate(guess):
            if result[i] == 'G':
                continue
            if g in answer_chars:
                result[i] = 'Y'
                answer_chars[answer_chars.index(g)] = None

        return ''.join(result)

    def is_consistent(self, word, guess, pattern):
        """Check if `word` would produce `pattern` given `guess`."""
        return self.get_feedback_pattern(guess, word) == pattern

    def filter_words(self, guess, pattern):
        """Remove all words that don't match feedback pattern."""
        self.possible_answers = [
            word for word in self.possible_answers
            if self.is_consistent(word, guess, pattern)
        ]
        print(f"{len(self.possible_answers)} word(s) remaining.")

    def calculate_entropy(self, guess):
        """Calculate expected information (entropy) of a guess."""
        pattern_counts = defaultdict(int)
        for answer in self.possible_answers:
            pattern = self.get_feedback_pattern(guess, answer)
            pattern_counts[pattern] += 1

        total = len(self.possible_answers)
        entropy = 0.0
        for count in pattern_counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def find_best_guess(self, round_num):
        # Precomputed best first guess
        if round_num == 1:
            self.input_first()
            return self.first_guess, self.calculate_entropy(self.first_guess)
        # Otherwise compute dynamically
        best_word = None
        best_entropy = -1
        for guess in self.all_guesses:
            ent = self.calculate_entropy(guess)
            if ent > best_entropy:
                best_entropy = ent
                best_word = guess
        return best_word, best_entropy

    def reset(self):
        """Reset to all words being possible again."""
        self.possible_answers = self.all_guesses.copy()

    def input_first(self):
        initial_guess = input("Please enter initial guess:").lower()
        if initial_guess in self.all_guesses:
            self.first_guess = initial_guess
        else:
            print("Word not in accepted list.")
            return self.input_first()

def handle_feedback():
    feedback = input("Enter feedback (e.g., BGBYY): ").strip().upper()
    if (len(feedback)==5) and (set(feedback).issubset({'B', 'G', 'Y'})):
        return feedback
    else:
        print("Feedback format not recognized.")
        return handle_feedback()

def main():

    print("Welcome to Wordle Solver!")
    print("Feedback codes: G=Green, Y=Yellow, B=Gray (e.g., BGBYY)")

    solver = WordleSolver("wordle_full_list.csv", )

    # Round loop
    for round_num in range(1, 7):
        print(f"\nRound {round_num}")
        guess, entropy = solver.find_best_guess(round_num)
        print(f"Suggested guess: {guess} (entropy {entropy:.4f})")

        #feedback = input("Enter feedback (e.g., BGBYY): ").strip().upper()
        feedback = handle_feedback()
        if feedback == "GGGGG":
            print("Wordle solved!")
            break

        solver.filter_words(guess, feedback)

        if len(solver.possible_answers) == 1:
            print(f"\nThe word must be: {solver.possible_answers[0]}")
            break
        elif not solver.possible_answers:
            print("No possible words remain in official Wordle list. (Check feedback input?)")
            break


if __name__ == "__main__":
    main()
