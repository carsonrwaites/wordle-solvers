from feedback import get_feedback_pattern

def play_game(answer, solver, allowed_words, first_guess="raise"):
    """
    Play one Wordle game:
    - answer: the hidden correct word
    - solver: instance of a class implementing SolverInterface
    - allowed_words: all valid guesses
    Returns:
        {
            'answer': str,
            'guesses': [str],
            'result': 'win' or 'loss'
        }
    """
    solver.reset(allowed_words, first_guess=first_guess)
    guesses = []

    for round_number in range(1, 7):
        guess = solver.get_guess(round_number)
        feedback = get_feedback_pattern(guess, answer)
        guesses.append(guess)

        if feedback == "GGGGG":
            return {
                "answer": answer,
                "guesses": guesses,
                "result": "win"
            }

        solver.process_feedback(guess, feedback)

    return {
        "answer": answer,
        "guesses": guesses,
        "result": "loss"
    }
