# minimax_solver.py
#from feedback import get_feedback_pattern
#from feedback_cache import get_feedback_pattern_cached as get_feedback_pattern
import feedback_cache
from solver_interface import SolverInterface
import math


class MinimaxSolver(SolverInterface):
    def reset(self, word_list, first_guess="raise"):
        self.possible_answers = list(word_list)
        self.all_guesses = list(word_list)
        self.first_guess = first_guess

    def get_guess(self, round_number):
        # First guess fixed
        if round_number == 1:
            return self.first_guess

        # If only one or two candidates left, guess them directly
        if len(self.possible_answers) <= 2:
            return self.possible_answers[0]

        best_guess = None
        best_worst_case = float('inf')
        best_entropy = -1

        for guess in self.all_guesses:
            # Map pattern -> number of words remaining
            pattern_groups = {}
            for answer in self.possible_answers:
                #pattern = get_feedback_pattern(guess, answer)
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