```python
def _read_input():
    import sys
    try:
        line1 = sys.stdin.readline()
        if not line1:
            return None
        n, r, c = map(int, line1.split())
        words = sys.stdin.readline().split()
    except (IOError, ValueError):
        return None
    return n, r, c, words


def _build_next_word(n, c, word_lens):
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


def _build_jump_table(next_word, n, r):
    max_log_r = r.bit_length()
    dp = [[0] * (n + 1) for _ in range(max_log_r)]
    dp[0] = next_word

    for k in range(1, max_log_r):
        for i in range(n + 1):
            dp[k][i] = dp[k - 1][dp[k - 1][i]]

    return dp, max_log_r


def _find_best_start(n, r, dp, max_log_r):
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


def _compute_best_segment(n, r, c, words):
    word_lens = [len(w) for w in words]
    next_word = _build_next_word(n, c, word_lens)
    dp, max_log_r = _build_jump_table(next_word, n, r)
    best_start, max_len = _find_best_start(n, r, dp, max_log_r)

    if max_len == 0:
        return None

    return best_start, max_len, next_word


def _print_layout(words, best_start, max_len, r, next_word):
    current_word_idx = best_start
    end_idx = best_start + max_len

    for _ in range(r):
        if current_word_idx >= end_idx:
            break

        line_end = next_word[current_word_idx]
        if line_end > end_idx:
            line_end = end_idx

        print(" ".join(words[current_word_idx:line_end]))
        current_word_idx = line_end


def solve():
    """
    Solves the Advertising problem using dynamic programming with binary lifting.
    The approach has a time complexity of O(N * log R) and space complexity of O(N * log R).
    """
    parsed_input = _read_input()
    if parsed_input is None:
        return

    n, r, c, words = parsed_input
    result = _compute_best_segment(n, r, c, words)
    if result is None:
        return

    best_start, max_len, next_word = result
    _print_layout(words, best_start, max_len, r, next_word)


def main():
    solve()


if __name__ == "__main__":
    main()
```

- Moved the previous top-level `solve()` call into `main()` under `if __name__ == "__main__":`, eliminating top-level execution while preserving script behavior.
- Kept the public `solve()` function name and signature unchanged; it now orchestrates well-separated helper functions.
- Extracted input reading into `_read_input()`, preserving the original `IOError`/`ValueError` handling and returning data instead of using implicit global state.
- Split the computation into focused helpers: `_build_next_word()`, `_build_jump_table()`, `_find_best_start()`, and `_compute_best_segment()`, with all data passed via parameters and return values.
- Moved output generation into `_print_layout()` and reused the already computed `next_word` table to avoid duplicating the greedy line-packing logic from the precomputation phase.
- Avoided module-level mutable state by keeping all runtime data local to functions.