```python
import sys


def read_configuration():
    line = sys.stdin.readline()
    if not line:
        return None
    t, m = map(int, line.split())
    return t, m


def read_operation():
    return sys.stdin.readline().strip()


def print_output(value):
    print(value)


def find_free_block(memory, m, n):
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


def allocate(memory, m, n, next_id, active_ids):
    found_pos = find_free_block(memory, m, n)

    if found_pos != -1:
        print_output(next_id)
        active_ids.add(next_id)
        for k in range(found_pos, found_pos + n):
            memory[k] = next_id
        return next_id + 1

    print_output("NULL")
    return next_id


def erase(memory, m, x, active_ids):
    if x > 0 and x in active_ids:
        active_ids.remove(x)
        for i in range(m):
            if memory[i] == x:
                memory[i] = 0
    else:
        print_output("ILLEGAL_ERASE_ARGUMENT")


def defragment(memory, m):
    occupied_blocks = [block for block in memory if block != 0]
    return occupied_blocks + [0] * (m - len(occupied_blocks))


def run_operations(t, m):
    memory = [0] * m
    next_id = 1
    active_ids = set()

    for _ in range(t):
        line = read_operation()
        if not line:
            continue

        parts = line.split()
        command = parts[0]

        if command == "alloc":
            n = int(parts[1])
            next_id = allocate(memory, m, n, next_id, active_ids)
        elif command == "erase":
            x = int(parts[1])
            erase(memory, m, x, active_ids)
        elif command == "defragment":
            memory = defragment(memory, m)


def memory_manager():
    """
    Implements a simple memory manager with alloc, erase, and defragment operations.
    """
    try:
        configuration = read_configuration()
        if configuration is None:
            return
        t, m = configuration
    except (IOError, ValueError):
        return

    run_operations(t, m)


def main():
    memory_manager()


if __name__ == "__main__":
    main()
```

- Separated input reading, computation, and output printing while keeping output at the point each operation produces it.
- Moved operation logic into helpers and kept memory state local to the simulation, passing it through parameters and return values.
- Preserved `memory_manager()` and its exception handling; the only top-level execution is the guarded `main()` call.