import sys


def read_input():
    """Read and parse input, returning (n, r, c, words) or None if input is invalid."""
    try:
        line1 = sys.stdin.readline()
        if not line1:
            return None
        n, r, c = map(int, line1.split())
        words = sys.stdin.readline().split()
        return n, r, c, words
    except (IOError, ValueError):
        return None


def compute_next_word_positions(word_lens, n, c):
    """
    Compute next_word[i] = index of first word that doesn't fit on a line starting with word i.
    Uses a sliding window approach with O(N) time complexity.
    """
    next_word = [0] * (n + 1)
    j = 0
    current_len = 0
    
    for i in range(n):
        # Slide window forward by removing word i-1
        if i > 0:
            current_len -= word_lens[i - 1]
            if j > i:
                current_len -= 1
        
        # Ensure j is at least i
        if j < i:
            j = i
            current_len = 0
        
        # Expand window with pointer j
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


def build_binary_lifting_table(next_word, n, max_log_r):
    """
    Build dp table for binary lifting.
    dp[k][i] = end position after 2^k lines starting from word i.
    """
    dp = [[0] * (n + 1) for _ in range(max_log_r)]
    dp[0] = next_word
    
    for k in range(1, max_log_r):
        for i in range(n + 1):
            dp[k][i] = dp[k - 1][dp[k - 1][i]]
    
    return dp


def find_best_starting_position(dp, n, r, max_log_r):
    """
    Find the starting position that maximizes the number of words that can be placed in r lines.
    Returns (best_start, max_len).
    """
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


def print_optimal_lines(words, word_lens, best_start, max_len, r, c):
    """Print the optimal r lines using greedy packing."""
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
    input_data = read_input()
    if input_data is None:
        return
    
    n, r, c, words = input_data
    word_lens = [len(w) for w in words]
    
    # Precompute next_word array
    next_word = compute_next_word_positions(word_lens, n, c)
    
    # Build binary lifting table
    max_log_r = r.bit_length()
    dp = build_binary_lifting_table(next_word, n, max_log_r)
    
    # Find best starting position
    best_start, max_len = find_best_starting_position(dp, n, r, max_log_r)
    
    # Print result
    if max_len == 0:
        return
    
    print_optimal_lines(words, word_lens, best_start, max_len, r, c)


solve()
