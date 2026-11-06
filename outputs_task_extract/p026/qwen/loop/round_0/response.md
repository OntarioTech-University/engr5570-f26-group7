```python
import sys


def memory_manager():
    """
    Implements a simple memory manager with alloc, erase, and defragment operations.
    """
    settings = read_initial_settings()
    if settings is None:
        return
    t, m = settings
    process_operations(t, m)


def read_initial_settings():
    try:
        line = sys.stdin.readline()
        if not line:
            return None
        t, m = map(int, line.split())
        return t, m
    except (IOError, ValueError):
        return None


def read_operation_line():
    return sys.stdin.readline().strip()


def parse_operation(line):
    return line.split()


def print_allocation_success(block_id):
    print(block_id)


def print_null():
    print("NULL")


def print_illegal_erase_argument():
    print("ILLEGAL_ERASE_ARGUMENT")


def find_first_fit(memory, m, n):
    i = 0
    while i <= m - n:
        if memory[i] == 0:
            j = i
            while j < m and memory[j] == 0:
                j += 1
            if j - i >= n:
                return i
            i = j
        else:
            i += 1
    return -1


def write_block(memory, start, n, block_id):
    for k in range(start, start + n):
        memory[k] = block_id


def handle_alloc(memory, m, active_ids, next_id, parts):
    n = int(parts[1])
    found_pos = find_first_fit(memory, m, n)
    if found_pos == -1:
        print_null()
        return next_id

    print_allocation_success(next_id)
    active_ids.add(next_id)
    write_block(memory, found_pos, n, next_id)
    return next_id + 1


def erase_block(memory, m, block_id):
    for i in range(m):
        if memory[i] == block_id:
            memory[i] = 0


def handle_erase(memory, m, active_ids, parts):
    x = int(parts[1])
    if x > 0 and x in active_ids:
        active_ids.remove(x)
        erase_block(memory, m, x)
    else:
        print_illegal_erase_argument()


def handle_defragment(memory, m):
    occupied_blocks = [block for block in memory if block != 0]
    return occupied_blocks + [0] * (m - len(occupied_blocks))


def process_operation_line(line, memory, m, active_ids, next_id):
    parts = parse_operation(line)
    command = parts[0]

    if command == "alloc":
        next_id = handle_alloc(memory, m, active_ids, next_id, parts)
    elif command == "erase":
        handle_erase(memory, m, active_ids, parts)
    elif command == "defragment":
        memory = handle_defragment(memory, m)

    return next_id, memory


def process_operations(t, m):
    memory = [0] * m
    next_id = 1
    active_ids = set()

    for _ in range(t):
        line = read_operation_line()
        if not line:
            continue
        next_id, memory = process_operation_line(
            line, memory, m, active_ids, next_id
        )


if __name__ == "__main__":
    memory_manager()
```

- Extracted initial input parsing into `read_initial_settings()` to isolate setup input handling while preserving the original EOF and exception behavior.
- Split operation input handling into `read_operation_line()` and `parse_operation()` so the main loop no longer mixes input reading with command processing.
- Moved allocation search logic into `find_first_fit()` and allocation writes into `write_block()` to separate the two main computation steps of `alloc`.
- Extracted all output statements into dedicated printing functions to keep side effects explicit and separate from control flow.
- Moved erase validation and memory clearing into `handle_erase()` and `erase_block()`, preserving the original order of validation, state mutation, and error reporting.
- Extracted defragmentation into `handle_defragment()` so memory compaction is isolated from command dispatch.
- Added `process_operation_line()` and `process_operations()` to keep `memory_manager()` short and focused on top-level orchestration only.