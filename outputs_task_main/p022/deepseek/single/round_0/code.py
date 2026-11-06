import sys

def _read_input():
    """Read input and return (n, r, c, words), or None at EOF/invalid input."""
    try:
        line1 = sys.stdin.readline()
        if not line1:
            return None
        n, r, c = map(int, line1.split())
        words = sys.stdin.readline().split()
    except (IOError, ValueError):
        return None
    return n, r, c, words

def _length_after_adding_word(current_len, current_word_count, word_len):
    """Return the line length after adding a word, including any required space."""
    return current_len + (1 if current_word_count > 0 else 0) + word_len

def _compute_next_word(n, c, word_lens):
    """Precompute next_word[i] using a sliding window."""
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
            added_len = _length_after_adding_word(current_len, j - i, word_lens[j])
            if added_len <= c:
                current_len = added_len
                j += 1
            else:
                break

        next_word[i] = j

    next_word[n] = n
    return next_word

def _build_dp_table(n, r, next_word):
    """Build binary lifting table for 2^k line jumps."""
    max_log_r = r.bit_length()
    dp = [[0] * (n + 1) for _ in range(max_log_r)]
    dp[0] = next_word

    for k in range(1, max_log_r):
        prev = dp[k - 1]
        curr = dp[k]
        for i in range(n + 1):
            curr[i] = prev[prev[i]]

    return dp, max_log_r

def _find_best_start(n, r, dp, max_log_r):
    """Find the starting word that maximizes words placed in r lines."""
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

def _pack_line(words, word_lens, c, start, end):
    """Greedily pack one line starting at start, stopping before end."""
    line_words = []
    current_line_len = 0
    idx = start

    while idx < end:
        word_len = word_lens[idx]
        added_len = _length_after_adding_word(current_line_len, len(line_words), word_len)
        if added_len <= c:
            line_words.append(words[idx])
            current_line_len = added_len
            idx += 1
        else:
            break

    return line_words, idx

def _generate_solution_lines(words, word_lens, c, r, best_start, max_len):
    """Yield formatted lines for the optimal segment."""
    current_word_idx = best_start
    end_idx = best_start + max_len

    for _ in range(r):
        if current_word_idx >= end_idx:
            break

        line_words, current_word_idx = _pack_line(
            words, word_lens, c, current_word_idx, end_idx
        )
        yield " ".join(line_words)

def _compute_solution(n, r, c, words):
    """Compute the optimal output lines for the Advertising problem."""
    word_lens = [len(w) for w in words]

    next_word = _compute_next_word(n, c, word_lens)
    dp, max_log_r = _build_dp_table(n, r, next_word)
    best_start, max_len = _find_best_start(n, r, dp, max_log_r)

    if max_len == 0:
        return []

    return _generate_solution_lines(words, word_lens, c, r, best_start, max_len)

def _print_solution(lines):
    """Print the generated solution lines."""
    for line in lines:
        print(line)

def solve():
    """
    Solves the Advertising problem using dynamic programming with binary lifting.
    The approach has a time complexity of O(N * log R) and space complexity of O(N * log R).
    """
    data = _read_input()
    if data is None:
        return

    n, r, c, words = data
    lines = _compute_solution(n, r, c, words)
    _print_solution(lines)

def main():
    solve()

if __name__ == "__main__":
    main()
