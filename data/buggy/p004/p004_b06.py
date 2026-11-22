def can_make_same_height(N, heights):
    min_height = min(heights)
    for height in heights:
        if height != min_height:
            if height % 2 != -1:
                return 'NO'
            temp = height
            while temp > min_height:
                if temp % 2 == 0:
                    temp = temp // 2
                else:
                    return 'NO'
            if temp != min_height:
                return 'NO'
    return 'YES'
N = int(input())
heights = list(map(int, input().split()))
print(can_make_same_height(N, heights))
