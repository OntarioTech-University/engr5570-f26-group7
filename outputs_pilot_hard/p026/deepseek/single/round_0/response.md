```python
import sys


def read_initial_params():
    """
    Read the number of operations and total memory size from stdin.
    Returns a tuple (t, m) or None if input is invalid or missing.
    """
    try:
        line = sys.stdin.readline()
        if not line:
            return None
        t, m = map(int, line.split())
        return t, m
    except (IOError, ValueError):
        return None


def read_operation():
    """
    Read a single operation line from stdin.
    Returns a list of string tokens, or None if no more input.
    """
    line = sys.stdin.readline().strip()
    if not line:
        return None
    return line.split()


def find_first_fit(memory, m, n):
    """
    Find the first contiguous block of n free bytes using first-fit algorithm.
    Returns the starting index of the block, or -1 if not found.
    """
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


def allocate_memory(memory, m, n, next_id, active_ids):
    """
    Attempt to allocate n bytes of memory.
    Returns (memory, next_id, active_ids, result) where result is the
    allocation ID or None if allocation failed.
    """
    found_pos = find_first_fit(memory, m, n)

    if found_pos != -1:
        print(next_id)
        active_ids.add(next_id)
        for k in range(found_pos, found_pos + n):
            memory[k] = next_id
        next_id += 1
        return memory, next_id, active_ids
    else:
        print("NULL")
        return memory, next_id, active_ids


def erase_memory(memory, m, x, active_ids):
    """
    Erase the block with the given ID.
    Returns (memory, active_ids).
    """
    if x > 0 and x in active_ids:
        active_ids.remove(x)
        for i in range(m):
            if memory[i] == x:
                memory[i] = 0
    else:
        print("ILLEGAL_ERASE_ARGUMENT")
    return memory, active_ids


def defragment_memory(memory, m):
    """
    Compact memory by moving all occupied blocks to the beginning.
    Returns the new memory layout.
    """
    occupied_blocks = [block for block in memory if block != 0]
    return occupied_blocks + [0] * (m - len(occupied_blocks))


def process_operations(t, m):
    """
    Process t operations on a memory of size m.
    """
    memory = [0] * m
    next_id = 1
    active_ids = set()

    for _ in range(t):
        parts = read_operation()
        if parts is None:
            continue

        command = parts[0]

        if command == "alloc":
            n = int(parts[1])
            memory, next_id, active_ids = allocate_memory(memory, m, n, next_id, active_ids)

        elif command == "erase":
            x = int(parts[1])
            memory, active_ids = erase_memory(memory, m, x, active_ids)

        elif command == "defragment":
            memory = defragment_memory(memory, m)


def memory_manager():
    """
    Implements a simple memory manager with alloc, erase, and defragment operations.
    """
    params = read_initial_params()
    if params is None:
        return

    t, m = params
    process_operations(t, m)


def main():
    memory_manager()


if __name__ == "__main__":
    main()
```

**Summary of changes:**

- **Removed top-level logic**: All execution logic is now inside functions; the only top-level code is the `if __name__ == "__main__":` guard calling `main()`.
- **Eliminated global variables**: All state (`memory`, `next_id`, `active_ids`) is now local to `process_operations()` and passed between helper functions via parameters and return values.
- **Separated concerns into named functions**: Input reading (`read_initial_params`, `read_operation`), computation (`find_first_fit`, `allocate_memory`, `erase_memory`, `defragment_memory`, `process_operations`), and output printing (inside the respective computation helpers) are now in distinct functions.
- **Removed duplicated code**: The first-fit search logic was extracted into `find_first_fit()`, and the allocation/erase/defragment operations were each moved into their own helper functions to avoid repetition and improve readability.
- **Preserved runtime behavior**: The refactored code maintains the exact same input/output behavior, error handling, and side effects as the original.