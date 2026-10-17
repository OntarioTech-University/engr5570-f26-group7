import sys


def _read_problem_input():
    """Read and parse input, returning None when input is missing or invalid."""
    try:
        line1 = sys.stdin.readline()
        if not line1:
            return None
        n, r, c = map(int, line1.split())
        words = sys.stdin.readline().split()
    except (IOError, ValueError):
        return None
    return n, r, c, words


def _compute_next_word(n, c, word_lens):
    """
    Precompute next_word using a two-pointer approach.

    next_word[i] is the index of the first word that does not fit on a line
    starting with word i.
    """
    next_word = [0] * (n + 1)
    j = 0
    current_len = 0

    for i in range(n):
        # Slide the window forward by removing word i-1.
        if i > 0:
            current_len -= word_lens[i - 1]
            if j > i:  # If there was more than one word, remove a space.
                current_len -= 1

        # Ensure j is at least i.
        if j < i:
            j = i
            current_len = 0

        # Expand the window with pointer j.
        while j < n:
            space = 1 if j > i else 0
            if current_len + space + word_lens[j] <= c:
                current_len += space + word_lens[j]
                j += 1
            else:
                break

        next_word[i] = j

    next_word[n] = n  # Sentinel value for out-of-bounds.
    return next_word


def _build_jump_table(next_word, r):
    """
    Build the binary lifting table.

    dp[k][i] is the end position after 2^k lines starting from i.
    """
    max_log_r = r.bit_length()
    size = len(next_word)
    dp = [[0] * size for _ in range(max_log_r)]
    dp[0] = next_word

    for k in range(1, max_log_r):
        previous = dp[k - 1]
        current = dp[k]
        for i in range(size):
            current[i] = previous[previous[i]]

    return dp


def _find_best_segment(dp, r, n):
    """Find the starting index that covers the maximum number of words in r lines."""
    max_len = 0
    best_start = -1
    max_log_r = len(dp)

    for start in range(n):
        current_pos = start

        # Decompose r into powers of 2 and jump accordingly.
        for k in range(max_log_r - 1, -1, -1):
            if (r >> k) & 1:
                current_pos = dp[k][current_pos]

        length = current_pos - start
        if length > max_len:
            max_len = length
            best_start = start

    return best_start, max_len


def _format_line(words, word_lens, current_word_idx, end_idx, c):
    """Greedily pack one line and return the line text plus the next word index."""
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

    return " ".join(line_words), current_word_idx


def _print_selected_lines(words, word_lens, best_start, max_len, r, c):
    """Print the greedily packed lines for the selected word segment."""
    current_word_idx = best_start
    end_idx = best_start + max_len

    for _ in range(r):
        if current_word_idx >= end_idx:
            break

        line, current_word_idx = _format_line(
            words, word_lens, current_word_idx, end_idx, c
        )
        print(line)


def solve():
    """
    Solves the Advertising problem using dynamic programming with binary lifting.
    The approach has a time complexity of O(N * log R) and space complexity of O(N * log R).
    """
    problem = _read_problem_input()
    if problem is None:
        return

    n, r, c, words = problem
    word_lens = [len(w) for w in words]

    next_word = _compute_next_word(n, c, word_lens)
    dp = _build_jump_table(next_word, r)
    best_start, max_len = _find_best_segment(dp, r, n)

    if max_len == 0:
        # This case happens if no single word can fit on a line.
        return

    _print_selected_lines(words, word_lens, best_start, max_len, r, c)


solve()
