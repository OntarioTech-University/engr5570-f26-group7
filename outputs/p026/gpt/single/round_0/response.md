```python
import sys


def _find_free_block(memory, memory_size, size):
    """Return the start of the first free block large enough, or -1."""
    i = 0
    while i <= memory_size - size:
        if memory[i] != 0:
            i += 1
            continue

        j = i
        while j < memory_size and memory[j] == 0:
            j += 1

        if j - i >= size:
            return i

        i = j

    return -1


def _erase_block(memory, memory_size, active_ids, block_id):
    if block_id > 0 and block_id in active_ids:
        active_ids.remove(block_id)
        for i in range(memory_size):
            if memory[i] == block_id:
                memory[i] = 0
    else:
        print("ILLEGAL_ERASE_ARGUMENT")


def _defragment(memory, memory_size):
    occupied_blocks = [block for block in memory if block != 0]
    return occupied_blocks + [0] * (memory_size - len(occupied_blocks))


def memory_manager():
    """
    Implements a simple memory manager with alloc, erase, and defragment operations.
    """
    try:
        line = sys.stdin.readline()
        if not line:
            return
        t, m = map(int, line.split())
    except (IOError, ValueError):
        return

    memory = [0] * m
    next_id = 1
    active_ids = set()

    for _ in range(t):
        line = sys.stdin.readline().strip()
        if not line:
            continue

        parts = line.split()
        command = parts[0]

        if command == "alloc":
            n = int(parts[1])
            found_pos = _find_free_block(memory, m, n)

            if found_pos != -1:
                print(next_id)
                active_ids.add(next_id)
                for k in range(found_pos, found_pos + n):
                    memory[k] = next_id
                next_id += 1
            else:
                print("NULL")

        elif command == "erase":
            x = int(parts[1])
            _erase_block(memory, m, active_ids, x)

        elif command == "defragment":
            memory = _defragment(memory, m)


if __name__ == "__main__":
    memory_manager()
```

- Extracted the first-fit search into a named function and removed a nested conditional, making the scan easier to follow.
- Moved erase and defragment logic into small helpers, leaving `memory_manager()` focused on processing commands.
- Kept the public interface and operation order unchanged.