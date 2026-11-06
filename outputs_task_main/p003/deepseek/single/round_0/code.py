def read_input():
    password = input().strip()
    n = int(input().strip())
    words = []
    for _ in range(n):
        words.append(input().strip())
    return password, words


def has_word_with_char_at(words, index, char):
    for word in words:
        if word[index] == char:
            return True
    return False


def can_form_password(password, words):
    if password in words:
        return True

    first_char_needed = password[0]
    second_char_needed = password[1]

    can_end_with_first = has_word_with_char_at(words, 1, first_char_needed)
    can_start_with_second = has_word_with_char_at(words, 0, second_char_needed)

    return can_end_with_first and can_start_with_second


def print_result(result):
    if result:
        print("YES")
    else:
        print("NO")


def main():
    password, words = read_input()
    result = can_form_password(password, words)
    print_result(result)


if __name__ == "__main__":
    main()
