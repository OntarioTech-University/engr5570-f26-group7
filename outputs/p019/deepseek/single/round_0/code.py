import heapq
from sys import stdin

def main():
    import sys
    data = sys.stdin.read().split()
    
    n, k, books = parse_input(data)
    
    ab, a_only, b_only = categorize_books(books)
    
    ab.sort()
    a_only.sort()
    b_only.sort()
    
    p_ab = make_prefix_sum(ab)
    p_a = make_prefix_sum(a_only)
    p_b = make_prefix_sum(b_only)
    
    min_time = find_minimum_time(k, p_ab, p_a, p_b, len(ab), len(a_only), len(b_only))
    
    print_result(min_time)

def parse_input(data):
    """Parse input data and return n, k, and list of books."""
    idx = 0
    n = int(data[idx])
    idx += 1
    k = int(data[idx])
    idx += 1
    
    books = []
    for _ in range(n):
        t = int(data[idx])
        idx += 1
        a = int(data[idx])
        idx += 1
        b = int(data[idx])
        idx += 1
        books.append((t, a, b))
    
    return n, k, books

def categorize_books(books):
    """Separate books into categories based on who likes them."""
    ab = []      # both like
    a_only = []  # alice only
    b_only = []  # bob only
    
    for t, a, b in books:
        if a == 1 and b == 1:
            ab.append(t)
        elif a == 1 and b == 0:
            a_only.append(t)
        elif a == 0 and b == 1:
            b_only.append(t)
        # Books that neither likes are ignored
    
    return ab, a_only, b_only

def make_prefix_sum(arr):
    """Create prefix sum array for quick sum calculation."""
    prefix = [0]
    running_sum = 0
    for value in arr:
        running_sum += value
        prefix.append(running_sum)
    return prefix

def find_minimum_time(k, p_ab, p_a, p_b, len_ab, len_a, len_b):
    """Find minimum time to satisfy both Alice and Bob's requirements."""
    min_time = float('inf')
    
    for cnt_ab in range(len_ab + 1):
        needed = max(0, k - cnt_ab)
        
        if needed > len_a or needed > len_b:
            continue
        
        total_time = p_ab[cnt_ab] + p_a[needed] + p_b[needed]
        min_time = min(min_time, total_time)
    
    return min_time

def print_result(min_time):
    """Print the result or -1 if no valid solution exists."""
    if min_time == float('inf'):
        print(-1)
    else:
        print(min_time)

if __name__ == "__main__":
    main()
