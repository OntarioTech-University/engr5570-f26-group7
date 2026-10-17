```python
def solve():
    """
    Solves a single test case for the Monk and Cakes problem.
    """
    try:
        # Read N (total numbers) and K (numbers to choose)
        n, k = map(int, input().split())

        # Read the list of N numbers
        numbers = list(map(int, input().split()))

        # Step 1: Calculate the number of set bits (cheesecakes) for each number.
        # We can use a list comprehension for a concise way to do this.
        # bin(num) converts a number to its binary string (e.g., 6 -> '0b110').
        # .count('1') counts the occurrences of '1' in that string.
        cheesecake_counts = [bin(num).count('1') for num in numbers]

        # Step 2: Sort the list of cheesecake counts in descending order.
        cheesecake_counts.sort(reverse=True)

        # Step 3: Sum the top K counts.
        # Slicing the list with [:k] gives us the first K elements.
        max_cakes = sum(cheesecake_counts[:k])

        # Print the final answer for the test case.
        print(max_cakes)

    except (ValueError, EOFError):
        # Handles potential errors with input, common in some online judges.
        pass

def main():
    """
    Main function to handle multiple test cases.
    """
    try:
        # Read the number of test cases
        t = int(input())
        for _ in range(t):
            solve()
    except (ValueError, EOFError):
        pass

if __name__ == "__main__":
    main()
```

- Left the file unchanged: the logic is already short and linear, with no complex conditionals or long functions that would benefit from splitting.