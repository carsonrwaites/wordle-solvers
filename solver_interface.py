# solver_interface.py
class SolverInterface:
    def reset(self, word_list):
        """
        Reset solver to a new game.
        word_list = full list of possible answers (fresh each game).
        """
        raise NotImplementedError

    def get_guess(self, round_number):
        """Return next guess as a string."""
        raise NotImplementedError

    def process_feedback(self, guess, feedback):
        """
        Process feedback pattern (like 'BGBYY') from previous guess.
        Allows solver to update internal state.
        """
        raise NotImplementedError
