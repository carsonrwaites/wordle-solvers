# entropy_solver.py
import math
from collections import defaultdict
from solver_interface import SolverInterface
# from feedback import get_feedback_pattern
from feedback_cache import get_feedback_pattern_cached as get_feedback_pattern

class EntropySolver(SolverInterface):
    def reset(self, word_list, first_guess="raise"):
        self.all_guesses = list(word_list)
        self.possible_answers = list(word_list)
        self.first_guess = first_guess

    def get_guess(self, round_number):
        # Hardcode first guess for speed
        if len(self.possible_answers) == 1:
            return self.possible_answers[0]

        if round_number == 1:
            return self.first_guess

        # Otherwise calculate entropy dynamically
        # print(f"DEBUG: {len(self.possible_answers)} candidates before selecting guess")
        best_word, best_entropy = None, -1
        for guess in self.all_guesses:
            ent = self.calculate_entropy(guess)
            if ent > best_entropy:
                best_entropy = ent
                best_word = guess
        return best_word

    def process_feedback(self, guess, feedback):
        # Filter possible answers based on feedback
        # print(f"DEBUG: Feedback for {guess} = {feedback}")
        old_count = len(self.possible_answers)
        self.possible_answers = [
            word for word in self.possible_answers
            if self.is_consistent(word, guess, feedback)
        ]
        #print(f"DEBUG: Candidates reduced from {old_count} to {len(self.possible_answers)}")
        #print(f"DEBUG: Remaining words are {self.possible_answers}")


    def calculate_entropy(self, guess):
        pattern_counts = defaultdict(int)
        for answer in self.possible_answers:
            pattern = get_feedback_pattern(guess, answer)
            pattern_counts[pattern] += 1

        total = len(self.possible_answers)
        entropy = 0.0
        for count in pattern_counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy


    def is_consistent(self, word, guess, pattern):
        # A word is consistent if it would produce the same feedback pattern
        return get_feedback_pattern(guess, word) == pattern
