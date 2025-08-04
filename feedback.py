# feedback.py
def get_feedback_pattern(guess, answer):
    """
    Compute Wordle feedback for guess vs answer.
    Output is a string of length 5 with:
        G = Green (correct letter & position)
        Y = Yellow (correct letter, wrong position)
        B = Black/Gray (letter not in word)
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
