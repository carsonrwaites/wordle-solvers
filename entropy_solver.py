import math
from collections import defaultdict
from solver_interface import SolverInterface
from feedback_cache import get_feedback_pattern_cached as get_feedback_pattern

class EntropySolver(SolverInterface):
    def reset(self, word_list, first_guess="raise"):
        self.all_guesses = list(word_list)
        self.possible_answers = list(word_list)
        self.first_guess = first_guess

    def get_guess(self, round_number):
        if len(self.possible_answers) == 1:
            return self.possible_answers[0]

        if round_number == 1:
            return self.first_guess

        best_word, best_entropy = None, -1
        for guess in self.all_guesses:
            ent = self.calculate_entropy(guess)
            if ent > best_entropy:
                best_entropy = ent
                best_word = guess
        return best_word

    def process_feedback(self, guess, feedback):
        self.possible_answers = [
            word for word in self.possible_answers
            if self.is_consistent(word, guess, feedback)
        ]

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
        return get_feedback_pattern(guess, word) == pattern
