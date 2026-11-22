import sys

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
    MAX_LOG_R = r.bit_length()
    dp = [[-1] * (n + 1) for _ in range(MAX_LOG_R)]
    dp[0] = next_word
    for k in range(1, MAX_LOG_R):
        for i in range(n + 1):
            dp[k][i] = dp[k - 1][dp[k - 1][i]]
    max_len = 0
    best_start = -1
    for i in range(n):
        current_pos = i
        for k in range(MAX_LOG_R - 1, -1, -1):
            if r >> k & 1:
                current_pos = dp[k][current_pos]
        length = current_pos - i
        if length > max_len:
            max_len = length
            best_start = i
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
            if current_line_len + space + word_len <= c:
                line_words.append(word)
                current_line_len += space + word_len
                current_word_idx += 1
            else:
                break
        print(' '.join(line_words))
solve()
