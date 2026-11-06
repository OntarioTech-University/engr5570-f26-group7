import sys


def _read_input():
    try:
        line1 = sys.stdin.readline()
        if not line1:
            return None
        n, r, c = map(int, line1.split())
        words = sys.stdin.readline().split()
        return n, r, c, words
    except (IOError, ValueError):
        return None


def _slide_window(i, j, current_len, word_lens):
    if i > 0:
        current_len -= word_lens[i - 1]
        if j > i:
            current_len -= 1
    if j < i:
        j = i
        current_len = 0
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


def _compute_next_word(n, c, word_lens):
    next_word = [0] * (n + 1)
    j = 0
    current_len = 0
    for i in range(n):
        j, current_len = _slide_window(i, j, current_len, word_lens)
        j, current_len = _expand_window(i, j, current_len, n, c, word_lens)
        next_word[i] = j
    next_word[n] = n
    return next_word


def _build_jump_table(n, r, next_word):
    max_log_r = r.bit_length()
    dp = [[0] * (n + 1) for _ in range(max_log_r)]
    dp[0] = next_word
    for k in range(1, max_log_r):
        for i in range(n + 1):
            dp[k][i] = dp[k - 1][dp[k - 1][i]]
    return dp


def _find_best_start(n, r, dp):
    max_len = 0
    best_start = -1
    for i in range(n):
        current_pos = i
        for k in range(r.bit_length() - 1, -1, -1):
            if (r >> k) & 1:
                current_pos = dp[k][current_pos]
        length = current_pos - i
        if length > max_len:
            max_len = length
            best_start = i
    return best_start, max_len


def _pack_line(current_word_idx, end_idx, c, words, word_lens):
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
    return current_word_idx, " ".join(line_words)


def _print_result(r, c, words, word_lens, best_start, max_len):
    if max_len == 0:
        return
    current_word_idx = best_start
    end_idx = best_start + max_len
    for _ in range(r):
        if current_word_idx >= end_idx:
            break
        current_word_idx, line = _pack_line(
            current_word_idx, end_idx, c, words, word_lens
        )
        print(line)


def solve():
    """
    Solves the Advertising problem using dynamic programming with binary lifting.
    The approach has a time complexity of O(N * log R) and space complexity of O(N * log R).
    """
    input_data = _read_input()
    if input_data is None:
        return
    n, r, c, words = input_data
    word_lens = [len(w) for w in words]
    next_word = _compute_next_word(n, c, word_lens)
    dp = _build_jump_table(n, r, next_word)
    best_start, max_len = _find_best_start(n, r, dp)
    _print_result(r, c, words, word_lens, best_start, max_len)


solve()
