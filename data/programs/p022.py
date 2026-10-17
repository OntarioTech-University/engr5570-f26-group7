import sys

def solve():
    """
    Solves the Advertising problem using dynamic programming with binary lifting.
    The approach has a time complexity of O(N * log R) and space complexity of O(N * log R).
    """
    try:
        # Read input using fast I/O
        line1 = sys.stdin.readline()
        if not line1: return
        n, r, c = map(int, line1.split())
        words = sys.stdin.readline().split()
    except (IOError, ValueError):
        return

    word_lens = [len(w) for w in words]

    # 1. Precompute next_word array using a two-pointer approach (O(N))
    # next_word[i] = index of the first word that doesn't fit on a line starting with word i
    next_word = [0] * (n + 1)
    j = 0
    current_len = 0
    for i in range(n):
        # Slide the window forward by removing word i-1
        if i > 0:
            current_len -= word_lens[i - 1]
            if j > i:  # If there was more than one word, remove a space
                current_len -= 1
        
        # Ensure j is at least i (it might have fallen behind if the window shrank to empty)
        if j < i:
            j = i
            current_len = 0

        # Expand the window with pointer j
        while j < n:
            space = 1 if j > i else 0
            if current_len + space + word_lens[j] <= c:
                current_len += space + word_lens[j]
                j += 1
            else:
                break
        next_word[i] = j
    next_word[n] = n  # Sentinel value for out-of-bounds

    # 2. Precompute dp table for binary lifting (O(N * log R))
    # dp[k][i] = end position after 2^k lines starting from i
    MAX_LOG_R = r.bit_length()
    dp = [[0] * (n + 1) for _ in range(MAX_LOG_R)]
    dp[0] = next_word

    for k in range(1, MAX_LOG_R):
        for i in range(n + 1):
            # Jump 2^(k-1) steps, then another 2^(k-1) steps from there
            dp[k][i] = dp[k - 1][dp[k - 1][i]]

    # 3. Find the best starting position (O(N * log R))
    max_len = 0
    best_start = -1

    for i in range(n):
        current_pos = i
        # Decompose r into powers of 2 and jump accordingly
        for k in range(MAX_LOG_R - 1, -1, -1):
            if (r >> k) & 1:
                current_pos = dp[k][current_pos]
        
        length = current_pos - i
        if length > max_len:
            max_len = length
            best_start = i

    # 4. Print the result
    if max_len == 0:
        # This case happens if no single word can fit on a line.
        return

    # Perform greedy packing for the optimal segment and print
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

solve()
