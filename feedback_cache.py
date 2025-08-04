# feedback_cache.py
import os
import pickle
from feedback import get_feedback_pattern as _get_feedback_pattern

_CACHE_FILE = "feedback_cache.pkl"
_feedback_cache = {}
_hits = 0
_misses = 0

def load_cache():
    global _feedback_cache
    if os.path.exists(_CACHE_FILE):
        with open(_CACHE_FILE, "rb") as f:
            _feedback_cache = pickle.load(f)
        print(f"[Feedback Cache] Loaded {_CACHE_FILE} with {len(_feedback_cache)} entries.")
    else:
        print("[Feedback Cache] No cache file found, starting empty.")

def save_cache():
    with open(_CACHE_FILE, "wb") as f:
        pickle.dump(_feedback_cache, f)
    print(f"[Feedback Cache] Saved {_CACHE_FILE} with {len(_feedback_cache)} entries.")
    print(f"[Feedback Cache Stats] Hits: {_hits}, Misses: {_misses}")

def get_feedback_pattern_cached(guess, answer):
    global _hits, _misses
    key = (guess, answer)
    if key in _feedback_cache:
        _hits += 1
        return _feedback_cache[key]
    else:
        _misses += 1
        pattern = _get_feedback_pattern(guess, answer)
        _feedback_cache[key] = pattern
        return pattern
