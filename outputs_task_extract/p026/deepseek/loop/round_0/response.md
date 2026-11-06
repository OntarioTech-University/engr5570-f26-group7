```python
import sys


def read_initial_params():
    """Read the first line and return (t, m), or None if input is missing/invalid."""
    try:
        line = sys.stdin.readline()
        if not line:
            return None
        t, m = map(int, line.split())
        return t, m
    except (IOError, ValueError):
        return None


def read_operation():
    """Read one operation line and return its parts, or None for an empty line."""
    line = sys.stdin.readline().strip()
    if not line:
        return None
    return line.split()


def find_first_fit(memory, m, n):
    """Return the starting index of the first contiguous free block of size n, or -1."""
    found_pos = -1
    i = 0
    while i <= m - n:
        if memory[i] == 0:
            j = i
            while j < m and memory[j] == 0:
                j += 1
            if (j - i) >= n:
                found_pos = i
                break
            else:
                i = j
        else:
            i += 1
    return found_pos


def allocate_memory(memory, start, size, block_id):
    """Mark the given range as occupied by block_id."""
    for k in range(start, start + size):
        memory[k] = block_id


def print_allocation(block_id):
    """Print a successful allocation ID."""
    print(block_id)


def erase_memory(memory, m, block_id):
    """Free all bytes belonging to block_id."""
    for i in range(m):
        if memory[i] == block_id:
            memory[i] = 0


def defragment_memory(memory, m):
    """Return a new memory list with all occupied blocks moved to the front."""
    occupied_blocks = [block for block in memory if block != 0]
    return occupied_blocks + [0] * (m - len(occupied_blocks))


def process_alloc(memory, m, next_id, active_ids, parts):
    """Handle an 'alloc' operation and return the updated next_id."""
    n = int(parts[1])
    found_pos = find_first_fit(memory, m, n)
    if found_pos != -1:
        print_allocation(next_id)
        active_ids.add(next_id)
        allocate_memory(memory, found_pos, n, next_id)
        return next_id + 1
    else:
        print("NULL")
        return next_id


def process_erase(memory, m, active_ids, parts):
    """Handle an 'erase' operation."""
    x = int(parts[1])
    if x > 0 and x in active_ids:
        active_ids.remove(x)
        erase_memory(memory, m, x)
    else:
        print("ILLEGAL_ERASE_ARGUMENT")


def process_defragment(memory, m):
    """Handle a 'defragment' operation and return the new memory list."""
    return defragment_memory(memory, m)


def process_operation(memory, m, next_id, active_ids, parts):
    """Dispatch a single operation to the appropriate handler."""
    command = parts[0]
    if command == "alloc":
        return process_alloc(memory, m, next_id, active_ids, parts), memory
    elif command == "erase":
        process_erase(memory, m, active_ids, parts)
        return next_id, memory
    elif command == "defragment":
        memory = process_defragment(memory, m)
        return next_id, memory
    else:
        return next_id, memory


def memory_manager():
    """
    Implements a simple memory manager with alloc, erase, and defragment operations.
    """
    params = read_initial_params()
    if params is None:
        return
    t, m = params

    memory = [0] * m
    next_id = 1
    active_ids = set()

    for _ in range(t):
        parts = read_operation()
        if parts is None:
            continue
        next_id, memory = process_operation(memory, m, next_id, active_ids, parts)


if __name__ == "__main__":
    memory_manager()
```