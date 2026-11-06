import sys


def _read_input():
    """
    Reads the problem input.

    Returns:
        tuple | None: (n, r, c, words) on success, or None if input is empty
        or cannot be parsed.
    """
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
    """Returns the lengths of all input words."""
    return [len(w) for w in words]


def _occupied_length(word_len, has_separator):
    """
    Returns the length occupied by a word, including a separating space
    when one is needed.
    """
    return word_len + (1 if has_separator else 0)


def _compute_next_word(word_lens, n, c):
    """
    Precomputes next_word.

    next_word[i] is the index of the first word that does not fit on a line
    starting with word i.
    """
    next_word = [0] * (n + 1)
    j = 0
    current_len = 0

    for i in range(n):
        # Slide the window forward by removing word i-1.
        if i > 0:
            current_len -= _occupied_length(word_lens[i - 1], j > i)

        # Ensure j is at least i.
        if j < i:
            j = i
            current_len = 0

        # Expand the window with pointer j.
        while j < n:
            added = _occupied_length(word_lens[j], j > i)
            if current_len + added <= c:
                current_len += added
                j += 1
            else:
                break

        next_word[i] = j

    next_word[n] = n
    return next_word


def _build_jump_table(next_word, n, r):
    """
    Builds the binary-lifting table.

    jump_table[k][i] is the end position after 2^k lines starting from i.
    """
    max_log_r = r.bit_length()
    jump_table = [[0] * (n + 1) for _ in range(max_log_r)]
    jump_table[0] = next_word

    for k in range(1, max_log_r):
        for i in range(n + 1):
            jump_table[k][i] = jump_table[k - 1][jump_table[k - 1][i]]

    return jump_table


def _find_best_start(jump_table, n, r):
    """
    Finds the starting index that covers the maximum number of words after
    r lines.
    """
    max_log_r = len(jump_table)
    max_len = 0
    best_start = -1

    for i in range(n):
        current_pos = i

        # Decompose r into powers of 2 and jump accordingly.
        for k in range(max_log_r - 1, -1, -1):
            if (r >> k) & 1:
                current_pos = jump_table[k][current_pos]

        length = current_pos - i
        if length > max_len:
            max_len = length
            best_start = i

    return max_len, best_start


def _compute_best_segment(n, r, c, word_lens):
    """Runs the main computation and returns the best segment."""
    next_word = _compute_next_word(word_lens, n, c)
    jump_table = _build_jump_table(next_word, n, r)
    return _find_best_start(jump_table, n, r)


def _print_layout(words, word_lens, best_start, max_len, r, c):
    """Prints the selected words using the original greedy line packing."""
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
            added = _occupied_length(word_len, bool(line_words))

            if current_line_len + added <= c:
                line_words.append(word)
                current_line_len += added
                current_word_idx += 1
            else:
                break

        print(" ".join(line_words))


def solve():
    """
    Solves the Advertising problem using dynamic programming with binary lifting.
    The approach has a time complexity of O(N * log R) and space complexity of O(N * log R).
    """
    parsed_input = _read_input()
    if parsed_input is None:
        return

    n, r, c, words = parsed_input
    word_lens = _word_lengths(words)

    max_len, best_start = _compute_best_segment(n, r, c, word_lens)

    if max_len == 0:
        return

    _print_layout(words, word_lens, best_start, max_len, r, c)


def main():
    solve()


if __name__ == "__main__":
    main()
