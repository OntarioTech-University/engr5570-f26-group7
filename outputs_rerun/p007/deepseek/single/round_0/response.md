```python
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def can_communicate_directly(pos1, pos2, R):
    return distance(pos1, pos2) <= R

def can_all_communicate(positions, R):
    """Return True if all three positions can communicate directly or via the third."""
    direct_links = [[False for _ in range(3)] for _ in range(3)]

    for i in range(3):
        for j in range(3):
            if i == j:
                direct_links[i][j] = True
            else:
                direct_links[i][j] = can_communicate_directly(positions[i], positions[j], R)

    for i in range(3):
        for j in range(i + 1, 3):
            # In a 3-node graph, the remaining index is the relay node.
            relay = 3 - i - j
            if not direct_links[i][j] and not (direct_links[i][relay] and direct_links[j][relay]):
                return False

    return True

def solve_case():
    R = int(input())
    chef = tuple(map(int, input().split()))
    head_server = tuple(map(int, input().split()))
    sous_chef = tuple(map(int, input().split()))

    positions = [chef, head_server, sous_chef]

    return "yes" if can_all_communicate(positions, R) else "no"

T = int(input())
for _ in range(T):
    print(solve_case())
```

- Extracted the connectivity check into `can_all_communicate(positions, R)` to separate direct-link construction from relay logic.
- Replaced the three repetitive nested `if` blocks with a single loop over unordered pairs, using `relay = 3 - i - j` to identify the third node.
- Renamed the internal matrix to `direct_links` to clarify that it stores only direct communication state.
- Preserved all public function signatures, input parsing, output values, and exception behavior.