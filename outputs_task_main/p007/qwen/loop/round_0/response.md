```python
import math


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def can_communicate_directly(pos1, pos2, R):
    return distance(pos1, pos2) <= R


def _read_int():
    return int(input())


def _read_position():
    return tuple(map(int, input().split()))


def _read_test_case_count():
    return _read_int()


def _read_case():
    R = _read_int()
    chef = _read_position()
    head_server = _read_position()
    sous_chef = _read_position()
    return R, chef, head_server, sous_chef


def _build_communication_matrix(positions, R):
    can_communicate = [[False for _ in range(3)] for _ in range(3)]

    for i in range(3):
        for j in range(3):
            if i == j:
                can_communicate[i][j] = True
            else:
                can_communicate[i][j] = can_communicate_directly(
                    positions[i],
                    positions[j],
                    R
                )

    return can_communicate


def _check_pair(all_can_communicate, can_communicate, first, second, relay):
    if not can_communicate[first][second]:
        if not (can_communicate[first][relay] and can_communicate[second][relay]):
            return False

    return all_can_communicate


def _compute_case(R, chef, head_server, sous_chef):
    positions = [chef, head_server, sous_chef]

    can_communicate = _build_communication_matrix(positions, R)

    all_can_communicate = True

    all_can_communicate = _check_pair(
        all_can_communicate,
        can_communicate,
        0,
        1,
        2
    )

    all_can_communicate = _check_pair(
        all_can_communicate,
        can_communicate,
        0,
        2,
        1
    )

    all_can_communicate = _check_pair(
        all_can_communicate,
        can_communicate,
        1,
        2,
        0
    )

    return "yes" if all_can_communicate else "no"


def solve_case():
    R, chef, head_server, sous_chef = _read_case()
    return _compute_case(R, chef, head_server, sous_chef)


def _print_result(result):
    print(result)


def main():
    test_case_count = _read_test_case_count()

    for _ in range(test_case_count):
        _print_result(solve_case())


if __name__ == "__main__":
    main()
```

- Moved the top-level test-case loop into `main()` and guarded it with `if __name__ == "__main__":`, eliminating top-level execution and global state.
- Added input helpers `_read_int`, `_read_position`, `_read_test_case_count`, and `_read_case` to isolate all stdin reading while preserving the original parsing order and conversions.
- Extracted the core computation into `_compute_case` and `_build_communication_matrix`, keeping `solve_case()`’s public signature and external behavior unchanged.
- Replaced the three repeated direct/indirect connectivity checks with the shared helper `_check_pair`.
- Added `_print_result` to isolate output printing.
- Preserved the public interfaces of `distance`, `can_communicate_directly`, and `solve_case`.