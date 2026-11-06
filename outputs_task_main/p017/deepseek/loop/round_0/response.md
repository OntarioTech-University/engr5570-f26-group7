Here's the refactored code:

```python
import sys
from collections import Counter


def read_input():
    """
    Reads and parses the input data.
    
    Returns:
        tuple: (n, a, m, queries) where n is the array length,
               a is the list of integers, m is the number of queries,
               and queries is a list of (k, pos) tuples.
    """
    input = sys.stdin.readline
    
    n_str = input()
    if not n_str:
        return None
    
    n = int(n_str)
    a = list(map(int, input().split()))
    m = int(input())
    
    queries = []
    for _ in range(m):
        k, pos = map(int, input().split())
        queries.append((k, pos))
    
    return n, a, m, queries


def compute_optimal_subsequences(n, a):
    """
    Computes the optimal subsequences for all possible k values.
    
    Args:
        n: Length of the array
        a: The input array
    
    Returns:
        dict: A cache mapping k to the optimal subsequence for that k
    """
    # Pair values with their original indices
    indexed_a = [(a[i], i) for i in range(n)]
    
    # Sort to find the elements for the max-sum subsequence
    indexed_a.sort(key=lambda x: (-x[0], x[1]))
    
    # Cache to store computed optimal subsequences for each k
    optimal_subs_cache = {}
    
    return indexed_a, optimal_subs_cache


def get_optimal_subsequence(k, indexed_a, optimal_subs_cache):
    """
    Gets or computes the optimal subsequence for a given k.
    
    Args:
        k: The number of elements to select
        indexed_a: The sorted array of (value, index) pairs
        optimal_subs_cache: Cache of previously computed subsequences
    
    Returns:
        list: The optimal subsequence for the given k
    """
    if k not in optimal_subs_cache:
        # Select the top k elements based on our sorting
        top_k_pairs = indexed_a[:k]
        
        # Reconstruct the subsequence by sorting by original index
        top_k_pairs.sort(key=lambda x: x[1])
        
        # Store the final sequence of values in the cache
        optimal_subs_cache[k] = [pair[0] for pair in top_k_pairs]
    
    return optimal_subs_cache[k]


def process_queries(queries, indexed_a, optimal_subs_cache):
    """
    Processes all queries and returns the results.
    
    Args:
        queries: List of (k, pos) tuples
        indexed_a: The sorted array of (value, index) pairs
        optimal_subs_cache: Cache of previously computed subsequences
    
    Returns:
        list: List of results for each query
    """
    results = []
    for k, pos in queries:
        optimal_subsequence = get_optimal_subsequence(k, indexed_a, optimal_subs_cache)
        result = optimal_subsequence[pos - 1]
        results.append(result)
    
    return results


def print_output(results):
    """
    Prints the results to stdout.
    
    Args:
        results: List of results to print
    """
    for result in results:
        sys.stdout.write(str(result) + '\n')


def solve():
    """
    Solves the optimal subsequence problem for the given input.
    """
    try:
        # Read input
        input_data = read_input()
        if input_data is None:
            return
        
        n, a, m, queries = input_data
        
        # Compute optimal subsequences
        indexed_a, optimal_subs_cache = compute_optimal_subsequences(n, a)
        
        # Process queries
        results = process_queries(queries, indexed_a, optimal_subs_cache)
        
        # Print output
        print_output(results)
        
    except (IOError, ValueError) as e:
        # Handle potential empty lines or format errors at the end of input
        pass


def main():
    solve()


if __name__ == "__main__":
    main()
```

**Changes made:**

- **Removed top-level logic**: All code that was previously at the module level is now inside functions, with only the `if __name__ == "__main__":` guard at the top level.
- **Eliminated global variables**: All variables are now local to their respective functions and passed as parameters where needed.
- **Separated concerns into functions**: 
  - `read_input()`: Handles all input parsing
  - `compute_optimal_subsequences()`: Sets up the data structures for computation
  - `get_optimal_subsequence()`: Computes or retrieves individual subsequences
  - `process_queries()`: Processes all queries and collects results
  - `print_output()`: Handles all output formatting and writing
- **Removed duplicated code**: The subsequence computation logic that was inline in the main loop is now extracted into `get_optimal_subsequence()`.
- **Added `main()` function**: Created a separate `main()` function that calls `solve()`, following the standard Python pattern.
- **Preserved behavior**: All error handling, input/output formats, and computation logic remain identical to the original code.