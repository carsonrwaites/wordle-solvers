import csv
from logger import Logger
from game_engine import play_game
from entropy_solver import EntropySolver
import multiprocessing as mp
from datetime import datetime
from minimax_solver import MinimaxSolver
from feedback_cache import load_cache, save_cache


def load_word_list(filename):
    with open(filename, 'r', encoding='utf-8-sig') as f:
        return [line.strip() for line in f if line.strip()]

def run_single_game(answer, word_list, first_guess):
    #solver = EntropySolver()
    solver = MinimaxSolver()
    result = play_game(answer=answer, solver=solver, allowed_words=word_list, first_guess=first_guess)
    return result

def run_all_answers(word_list, first_guess, n_processes=8):
    logger = Logger()
    tasks = [(answer, word_list, first_guess) for answer in word_list]

    with mp.Pool(processes=n_processes) as pool:
        results = pool.starmap(run_single_game, tasks)

    for result in results:
        logger.log_game(result)

    logger.dump_results_to_file(f"results/minimax_{first_guess}_results.txt")

def main():
    load_cache()
    word_list = load_word_list("wordle_full_list.csv")

    #starters = ["stale", "saner", "alter", "later", "react", "trade", "leant", "learn", "roast"]
    starters = ['stale']

    for starter in starters:
        print(f"Starting analysis on: {starter}.")
        run_all_answers(word_list, starter)

    save_cache()


if __name__ == "__main__":
    print(datetime.now())

    main()

    print(datetime.now())
