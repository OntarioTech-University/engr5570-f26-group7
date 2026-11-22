def rotate_90_clockwise(x, y):
    return (y, -x)

def gcd(a, b):
    while b:
        a, b = (b, a % b)
    return abs(a)

def main():
    line = input().split()
    x1, y1 = (int(line[0]), int(line[1]))
    line = input().split()
    x2, y2 = (int(line[0]), int(line[1]))
    line = input().split()
    x3, y3 = (int(line[0]), int(line[1]))
    c_vectors = [(x3, y3)]
    for _ in range(3):
        c_vectors.append(rotate_90_clockwise(c_vectors[-1][0], c_vectors[-1][1]))
    current_a = (x1, y1)
    for rot in range(4):
        target_x = x2 - current_a[0]
        target_y = y2 - current_a[1]
        if target_x == 0 and target_y == 0:
            print('YES')
            return
        found = False
        for i in range(4):
            vx, vy = c_vectors[i]
            if vx != 0 and target_x % vx == 0:
                k = target_x // vx
                if k >= 0 and k * vy == target_y:
                    found = True
                    break
            elif vy != 0 and target_y % vy == 0:
                k = target_y // vy
                if k >= 0 and k * vx == target_x:
                    found = True
                    break
            elif vx == 0 and vy == 0 and (target_x == 0) and (target_y == 0):
                found = True
                break
        if found:
            print('YES')
            return
        for i in range(4):
            for j in range(i + 1, 4):
                v1x, v1y = c_vectors[i]
                v2x, v2y = c_vectors[j]
                det = v1x * v2y - v1y * v2x
                if det != 0:
                    if (v2y * target_x - v2x * target_y) % det == 0 and (v1x * target_y + v1y * target_x) % det == 0:
                        a = (v2y * target_x - v2x * target_y) // det
                        b = (v1x * target_y - v1y * target_x) // det
                        if a >= 0 and b >= 0:
                            found = True
                            break
                else:
                    cross = v1x * target_y - v1y * target_x
                    if cross == 0:
                        if v1x != 0:
                            if target_x % v1x == 0:
                                a = target_x // v1x
                                if a >= 0 and a * v1y == target_y:
                                    found = True
                                    break
                        elif v1y != 0:
                            if target_y % v1y == 0:
                                a = target_y // v1y
                                if a >= 0 and a * v1x == target_x:
                                    found = True
                                    break
                        elif target_x == 0 and target_y == 0:
                            found = True
                            break
            if found:
                break
        if found:
            print('YES')
            return
        current_a = rotate_90_clockwise(current_a[0], current_a[1])
    print('NO')
if __name__ == '__main__':
    main()
