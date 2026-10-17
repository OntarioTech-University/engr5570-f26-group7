```python
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def can_communicate_directly(pos1, pos2, R):
    return distance(pos1, pos2) <= R

def _read_position():
    return tuple(map(int, input().split()))

def _pair_can_communicate(positions, i, j, R):
    if i == j:
        return True
    return can_communicate_directly(positions[i], positions[j], R)

def _build_communication_matrix(positions, R):
    return [
        [_pair_can_communicate(positions, i, j, R) for j in range(3)]
        for i in range(3)
    ]

def _all_can_communicate(can_communicate):
    chef_head_server = can_communicate[0][1]
    chef_sous_chef = can_communicate[0][2]
    head_server_sous_chef = can_communicate[1][2]

    # With three participants, the group is connected exactly when
    # at least two of the three pairwise direct links exist.
    return (
        (chef_head_server and chef_sous_chef)
        or (chef_head_server and head_server_sous_chef)
        or (chef_sous_chef and head_server_sous_chef)
    )

def solve_case():
    R = int(input())
    chef = _read_position()
    head_server = _read_position()
    sous_chef = _read_position()

    positions = [chef, head_server, sous_chef]
    can_communicate = _build_communication_matrix(positions, R)

    return "yes" if _all_can_communicate(can_communicate) else "no"

T = int(input())
for _ in range(T):
    print(solve_case())
```

- Extracted `_read_position()` to remove repeated input-parsing logic and make `solve_case()` easier to read.
- Extracted `_pair_can_communicate()` and `_build_communication_matrix()` to separate communication-matrix construction from the main case logic while preserving the original pair-checking behavior.
- Replaced the three repeated connectivity checks with `_all_can_communicate()`, which expresses the same three-node connectivity rule more directly.
- Kept all public function names, signatures, top-level execution flow, inputs, outputs, and return values unchanged.