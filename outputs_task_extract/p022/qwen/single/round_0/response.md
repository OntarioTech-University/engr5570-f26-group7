```python
import sys


def _read_input():
    try:
        line1 = sys.stdin.readline()
        if not line1:
            return None
        n, r, c = map(int, line1.split())
        words = sys.stdin.readline().split()
    except (IOError, ValueError):
        return None
    return n, r, c, words


def _word_lengths(words):
    return [len(w) for w in words]


def _remove_previous_word(i, j, current_len, word_lens):
    if i > 0:
        current_len -= word_lens[i - 1]
        if j > i:
            current_len -= 1
    return j, current_len


def _reset_window_if_empty(i, j, current_len):
    if j < i:
        return i, 0
    return j, current_len


def _expand_window(i, j, current_len, n, c, word_lens):
    while j < n:
        space = 1 if j > i else 0
        if current_len + space + word_lens[j] <= c:
            current_len += space + word_lens[j]
            j += 1
        else:
            break
    return j, current_len


def _compute_next_word(word_lens, n, c):
    next_word = [0] * (n + 1)
    j = 0
    current_len = 0
    for i in range(n):
        j, current_len = _remove_previous_word(i, j, current_len, word_lens)
        j, current_len = _reset_window_if_empty(i, j, current_len)
        j, current_len = _expand_window(i, j, current_len, n, c, word_lens)
        next_word[i] = j
    next_word[n] = n
    return next_word


def _fill_dp_level(dp, k, n):
    prev = dp[k - 1]
    curr = dp[k]
    for i in range(n + 1):
        curr[i] = prev[prev[i]]


def _build_dp_table(next_word, n, r):
    max_log_r = r.bit_length()
    dp = [[0] * (n + 1) for _ in range(max_log_r)]
    dp[0] = next_word
    for k in range(1, max_log_r):
        _fill_dp_level(dp, k, n)
    return dp


def _words_covered(dp, start, r):
    current_pos = start
    max_log_r = r.bit_length()
    for k in range(max_log_r - 1, -1, -1):
        if (r >> k) & 1:
            current_pos = dp[k][current_pos]
    return current_pos - start


def _find_best_start(dp, n, r):
    max_len = 0
    best_start = -1
    for i in range(n):
        length = _words_covered(dp, i, r)
        if length > max_len:
            max_len = length
            best_start = i
    return best_start, max_len


def _build_line(words, word_lens, current_word_idx, end_idx, c):
    line_words = []
    current_line_len = 0
    while current_word_idx < end_idx:
        word = words[current_word_idx]
        word_len = word_lens[current_word_idx]
        space = 1 if line_words else 0
        if current_line_len + space + word_len <= c:
            line_words.append(word)
            current_line_len += space + word_len
            current_word_idx += 1
        else:
            break
    return current_word_idx, line_words


def _print_result(words, word_lens, best_start, max_len, r, c):
    if max_len == 0:
        return
    current_word_idx = best_start
    end_idx = best_start + max_len
    for _ in range(r):
        if current_word_idx >= end_idx:
            break
        current_word_idx, line_words = _build_line(words, word_lens, current_word_idx, end_idx, c)
        print(" ".join(line_words))


def solve():
    """
    Solves the Advertising problem using dynamic programming with binary lifting.
    The approach has a time complexity of O(N * log R) and space complexity of O(N * log R).
    """
    data = _read_input()
    if data is None:
        return
    n, r, c, words = data
    word_lens = _word_lengths(words)
    next_word = _compute_next_word(word_lens, n, c)
    dp = _build_dp_table(next_word, n, r)
    best_start, max_len = _find_best_start(dp, n, r)
    _print_result(words, word_lens, best_start, max_len, r, c)


solve()
```

- Extracted input reading into `_read_input()` so parsing and early-return/error handling are isolated from the main algorithm.
- Split the two-pointer `next_word` construction into `_compute_next_word()` plus tiny helpers, making each sliding-window adjustment explicit and short.
- Separated binary-lifting table construction into `_build_dp_table()` and `_fill_dp_level()`, keeping the recurrence logic in its own focused function.
- Moved the per-start-position jump evaluation into `_words_covered()` and the overall best-segment search into `_find_best_start()`.
- Moved output generation into `_print_result()` and line construction into `_build_line()`, so printing logic is separate from computation.
- Kept `solve()` as the unchanged public entry point and preserved the unconditional top-level `solve()` call to maintain runtime behavior.