def can_make_same_height(N, heights):
    min_height = _find_minimum_height(heights)
    return _check_all_heights(heights, min_height)


def _find_minimum_height(heights):
    return min(heights)


def _check_all_heights(heights, min_height):
    for height in heights:
        if not _can_match_minimum_height(height, min_height):
            return "NO"
    return "YES"


def _can_match_minimum_height(height, min_height):
    if height != min_height:
        if height % 2 != 0:
            return False
        return _can_reduce_to_minimum_height(height, min_height)
    return True


def _can_reduce_to_minimum_height(height, min_height):
    temp = height
    while temp > min_height:
        if temp % 2 == 0:
            temp = temp // 2
        else:
            return False

    if temp != min_height:
        return False
    return True


def _read_number_of_sugarcanes():
    return int(input())


def _read_heights():
    return list(map(int, input().split()))


def _print_result(result):
    print(result)


def _main():
    N = _read_number_of_sugarcanes()
    heights = _read_heights()
    _print_result(can_make_same_height(N, heights))


_main()
