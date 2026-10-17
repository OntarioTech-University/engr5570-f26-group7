# Read input
password = input().strip()
n = int(input().strip())
words = [input().strip() for _ in range(n)]


def can_form_password(password, words):
    """Check if password can be formed from the given words."""
    if password in words:
        return True

    first_char_needed = password[0]
    second_char_needed = password[1]

    can_end_with_first = any(word[1] == first_char_needed for word in words)
    can_start_with_second = any(word[0] == second_char_needed for word in words)

    return can_end_with_first and can_start_with_second


if can_form_password(password, words):
    print("YES")
else:
    print("NO")
