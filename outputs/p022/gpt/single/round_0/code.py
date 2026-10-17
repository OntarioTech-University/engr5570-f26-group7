import sys


def _compute_next_word(word_lens, n, c):
    """Find the first word that does not fit on each possible line."""
    next_word = [0] * (n + 1)
    j = 0
    current_len = 0

    for i in range(n):
        if i > 0:
            current_len -= word_lens[i - 1]
            if j > i:
                current_len -= 1

        if j < i:
            j = i
            current_len = 0

        while j < n:
            space = 1 if j > i else 0
            if current_len + space + word_lens[j] <= c:
                current_len += space + word_lens[j]
                j += 1
            else:
                break

        next_word[i] = j

    next_word[n] = n
    return next_word


def _build_jump_table(next_word, n, max_log_r):
    """Build positions reached after powers of two lines."""
    dp = [[0] * (n + 1) for _ in range(max_log_r)]
    dp[0] = next_word

    for k in range(1, max_log_r):
        for i in range(n + 1):
            dp[k][i] = dp[k - 1][dp[k - 1][i]]

    return dp


def _find_best_start(dp, n, r, max_log_r):
    max_len = 0
    best_start = -1

    for i in range(n):
        current_pos = i
        for k in range(max_log_r - 1, -1, -1):
            if (r >> k) & 1:
                current_pos = dp[k][current_pos]

        length = current_pos - i
        if length > max_len:
            max_len = length
            best_start = i

    return best_start, max_len


def _print_lines(words, word_lens, best_start, max_len, r, c):
    current_word_idx = best_start
    end_idx = best_start + max_len

    for _ in range(r):
        if current_word_idx >= end_idx:
            break

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

        print(" ".join(line_words))


def solve():
    """
    Solves the Advertising problem using dynamic programming with binary lifting.
    The approach has a time complexity of O(N * log R) and space complexity of O(N * log R).
    """
    try:
        line1 = sys.stdin.readline()
        if not line1:
            return
        n, r, c = map(int, line1.split())
        words = sys.stdin.readline().split()
    except (IOError, ValueError):
        return

    word_lens = [len(w) for w in words]
    next_word = _compute_next_word(word_lens, n, c)

    max_log_r = r.bit_length()
    dp = _build_jump_table(next_word, n, max_log_r)
    best_start, max_len = _find_best_start(dp, n, r, max_log_r)

    if max_len == 0:
        return

    _print_lines(words, word_lens, best_start, max_len, r, c)


solve()
