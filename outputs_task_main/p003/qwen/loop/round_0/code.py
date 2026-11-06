def read_input():
    password = input().strip()
    n = int(input().strip())
    words = []
    for _ in range(n):
        words.append(input().strip())
    return password, words


def _has_word_with_char_at(words, char, index):
    for word in words:
        if word[index] == char:
            return True
    return False


def compute_result(password, words):
    if password in words:
        return "YES"

    first_char_needed = password[0]
    second_char_needed = password[1]

    can_end_with_first = _has_word_with_char_at(words, first_char_needed, 1)
    can_start_with_second = _has_word_with_char_at(words, second_char_needed, 0)

    if can_end_with_first and can_start_with_second:
        return "YES"
    return "NO"


def print_result(result):
    print(result)


def main():
    password, words = read_input()
    result = compute_result(password, words)
    print_result(result)


if __name__ == "__main__":
    main()
