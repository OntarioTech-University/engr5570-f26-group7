def count_balanced_substrings(s):
    count = 0
    n = len(s)
    for l in range(n):
        for r in range(l, n):
            for x in range(l, r + 1):
                left_4 = s[l:x].count('4')
                right_7 = s[x:r + 1].count('7')
                if left_4 == right_7:
                    count += 1
                    break
    return count


def read_input():
    t = int(input())
    test_cases = []
    for _ in range(t):
        test_cases.append(input())
    return test_cases


def process_test_cases(test_cases):
    results = []
    for s in test_cases:
        results.append(count_balanced_substrings(s))
    return results


def print_results(results):
    for result in results:
        print(result)


def main():
    test_cases = read_input()
    results = process_test_cases(test_cases)
    print_results(results)


if __name__ == "__main__":
    main()
