```python
import sys


def read_input():
    """Read the advertising parameters and words."""
    try:
        line1 = sys.stdin.readline()
        if not line1:
            return None
        n, r, c = map(int, line1.split())
        words = sys.stdin.readline().split()
    except (IOError, ValueError):
        return None

    return n, r, c, words


def fits_on_line(current_length, space, word_length, width):
    return current_length + space + word_length <= width


def build_next_word(n, c, word_lens):
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
            if fits_on_line(current_len, space, word_lens[j], c):
                current_len += space + word_lens[j]
                j += 1
            else:
                break

        next_word[i] = j

    next_word[n] = n
    return next_word


def build_jump_table(n, r, next_word):
    """Build the binary-lifting table for line transitions."""
    max_log_r = r.bit_length()
    dp = [[0] * (n + 1) for _ in range(max_log_r)]
    dp[0] = next_word

    for k in range(1, max_log_r):
        for i in range(n + 1):
            dp[k][i] = dp[k - 1][dp[k - 1][i]]

    return dp


def find_best_segment(n, r, dp):
    """Find the starting position that fits the most words."""
    max_len = 0
    best_start = -1
    max_log_r = r.bit_length()

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


def compute_result(n, r, c, words):
    """Compute the optimal segment and retain lengths for printing."""
    word_lens = [len(w) for w in words]
    next_word = build_next_word(n, c, word_lens)
    dp = build_jump_table(n, r, next_word)
    best_start, max_len = find_best_segment(n, r, dp)
    return best_start, max_len, word_lens


def print_result(r, c, words, best_start, max_len, word_lens):
    """Greedily pack and print the optimal segment."""
    if max_len == 0:
        return

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

            if fits_on_line(current_line_len, space, word_len, c):
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
    input_data = read_input()
    if input_data is None:
        return

    n, r, c, words = input_data
    best_start, max_len, word_lens = compute_result(n, r, c, words)
    print_result(r, c, words, best_start, max_len, word_lens)


def main():
    solve()


if __name__ == "__main__":
    main()
```

- Separated input reading, computation, and printing into functions that exchange data through parameters and return values.
- Extracted the shared line-fit check and named the computation steps to reduce duplication and clarify their roles.
- Kept `solve()` unchanged as a public interface and moved its top-level call under the `main()` guard.