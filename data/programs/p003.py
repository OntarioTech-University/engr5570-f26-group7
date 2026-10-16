# Read input
password = input().strip()
n = int(input().strip())
words = []
for _ in range(n):
    words.append(input().strip())

# Check if password exists as a word
if password in words:
    print("YES")
else:
    # Check if we can form password across word boundaries
    first_char_needed = password[0]
    second_char_needed = password[1]
    
    # Find if there's a word ending with first_char_needed
    can_end_with_first = False
    for word in words:
        if word[1] == first_char_needed:
            can_end_with_first = True
            break
    
    # Find if there's a word starting with second_char_needed
    can_start_with_second = False
    for word in words:
        if word[0] == second_char_needed:
            can_start_with_second = True
            break
    
    if can_end_with_first and can_start_with_second:
        print("YES")
    else:
        print("NO")
