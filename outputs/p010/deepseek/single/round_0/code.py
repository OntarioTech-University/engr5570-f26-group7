def count_set_bits(number):
    """
    Count the number of set bits (1s) in the binary representation of a number.
    """
    return bin(number).count('1')


def read_numbers():
    """
    Read a line of space-separated integers from input.
    """
    return list(map(int, input().split()))


def get_max_cheesecakes(numbers, k):
    """
    Calculate the maximum number of cheesecakes by selecting K numbers
    with the highest set bit counts.
    """
    cheesecake_counts = [count_set_bits(num) for num in numbers]
    cheesecake_counts.sort(reverse=True)
    return sum(cheesecake_counts[:k])


def solve():
    """
    Solves a single test case for the Monk and Cakes problem.
    """
    try:
        n, k = read_numbers()
        numbers = read_numbers()
        max_cakes = get_max_cheesecakes(numbers, k)
        print(max_cakes)
    except (ValueError, EOFError):
        pass


def main():
    """
    Main function to handle multiple test cases.
    """
    try:
        t = int(input())
        for _ in range(t):
            solve()
    except (ValueError, EOFError):
        pass


if __name__ == "__main__":
    main()
