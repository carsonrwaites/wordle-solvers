import math
import feedback_cache
from solver_interface import SolverInterface


class MinimaxSolver(SolverInterface):
    def reset(self, word_list, first_guess="raise"):
        self.possible_answers = list(word_list)
        self.all_guesses = list(word_list)
        self.first_guess = first_guess

    def get_guess(self, round_number):
        if round_number == 1:
            return self.first_guess

        if len(self.possible_answers) <= 2:
            return self.possible_answers[0]

        best_guess = None
        best_worst_case = float('inf')
        best_entropy = -1

        for guess in self.all_guesses:
            # Map pattern -> number of words remaining
            pattern_groups = {}
            for answer in self.possible_answers:
                pattern = feedback_cache.get_feedback_pattern_cached(guess, answer)
                pattern_groups[pattern] = pattern_groups.get(pattern, 0) + 1

            worst_case = max(pattern_groups.values())
            total = sum(pattern_groups.values())
            entropy = -sum((c/total) * math.log2(c/total)
                           for c in pattern_groups.values())

            # Choose minimax, break ties on entropy
            if (worst_case < best_worst_case or
                (worst_case == best_worst_case and entropy > best_entropy)):
                best_worst_case = worst_case
                best_entropy = entropy
                best_guess = guess
        return best_guess


    def process_feedback(self, guess, feedback):
        self.possible_answers = [
            word for word in self.possible_answers
            if feedback_cache.get_feedback_pattern_cached(guess, word) == feedback
        ]
        print(f"{len(self.possible_answers)} word(s) remaining.")


def handle_feedback():
    feedback = input("Enter feedback (e.g., BGBYY): ").strip().upper()
    if (len(feedback)==5) and (set(feedback).issubset({'B', 'G', 'Y'})):
        return feedback
    else:
        print("Feedback format not recognized.")
        return handle_feedback()

def load_words(filename):
    # CSV file, one word per line, utf-8-sig encoding
    with open(filename, 'r', encoding='utf-8-sig') as f:
        return [line.strip() for line in f if line.strip()]

def input_first(word_list):
    initial_guess = input("Please enter initial guess:").lower()
    if initial_guess in word_list:
        return initial_guess
    else:
        print("Word not in accepted list.")
        return input_first(word_list)

def main():
    print("Welcome to Wordle Solver!")
    print("Feedback codes: G=Green, Y=Yellow, B=Gray (e.g., BGBYY)")
    word_list = load_words("wordle_full_list.csv")
    first_guess = input_first(word_list)

    solver = MinimaxSolver()
    solver.reset(word_list, first_guess=first_guess)

    for round_num in range(1, 7):
        print(f"\nRound {round_num}")
        guess = solver.get_guess(round_num)
        print(f"Suggested guess: {guess}")

        feedback = handle_feedback()
        if feedback == "GGGGG":
            print("Wordle solved!")
            break

        solver.process_feedback(guess, feedback)

        if len(solver.possible_answers) == 1:
            print(f"\nThe word must be: {solver.possible_answers[0]}")
            break
        elif not solver.possible_answers:
            print("No possible words remain in official Wordle list. (Check feedback input?)")
            break


if __name__ == "__main__":
    main()
