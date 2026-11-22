r1, r2 = map(int, input().split())
c1, c2 = map(int, input().split())
d1, d2 = map(int, input().split())
found = False
result = []
for a in range(1, 10):
    b = r1 - a
    c = c1 - a
    d = d1 - a
    if 1 <= b <= 9 and 1 <= c <= 9 and (1 <= d <= 9):
        s = {a, b, c, d}
        if len(s) == 4:
            if c + d == r2 or b + d == c2 or b + c == d2:
                found = True
                result = [[a, b], [c, d]]
                break
if found:
    print(result[0][0], result[0][1])
    print(result[1][0], result[1][1])
else:
    print(-1)
