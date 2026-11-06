```python
def read_initial_parameters():
    t, m = map(int, input().split())
    return t, m


def read_operation_parts():
    return input().strip().split()


def set_memory_range(memory, start, length, occupied):
    for i in range(start, start + length):
        memory[i] = occupied


def find_first_fit(memory, m, n):
    for i in range(1, m - n + 2):
        valid = True
        for j in range(i, i + n):
            if memory[j]:
                valid = False
                break
        if valid:
            return i
    return None


def allocate_block(memory, m, n, blocks, active_ids, next_id):
    pos = find_first_fit(memory, m, n)
    if pos is None:
        return "NULL", next_id

    set_memory_range(memory, pos, n, True)
    blocks.append((next_id, pos, n))
    active_ids.add(next_id)

    return str(next_id), next_id + 1


def find_block(blocks, block_id):
    for index in range(len(blocks)):
        b_id, start, length = blocks[index]
        if b_id == block_id:
            return index, start, length
    return None


def erase_block(blocks, memory, active_ids, block_id):
    found = find_block(blocks, block_id)
    if found is None:
        return

    index, start, length = found
    set_memory_range(memory, start, length, False)
    del blocks[index]
    active_ids.discard(block_id)


def defragment_blocks(blocks, memory, m):
    blocks.sort(key=lambda b: b[1])

    current_pos = 1
    new_blocks = []

    for b_id, old_start, length in blocks:
        end_pos = current_pos + length - 1
        if end_pos > m:
            continue

        set_memory_range(memory, old_start, length, False)
        set_memory_range(memory, current_pos, length, True)

        new_blocks.append((b_id, current_pos, length))
        current_pos += length

    return new_blocks


def simulate(t, m):
    # Memory representation: True means occupied
    memory = [False] * (m + 1)  # 1-based indexing

    # List of blocks: (id, start, length)
    blocks = []

    # Keep track of next id to assign
    next_id = 1

    # Set of currently active ids
    active_ids = set()

    result = []

    for _ in range(t):
        parts = read_operation_parts()
        op = parts[0]

        if op == "alloc":
            n = int(parts[1])
            line, new_next_id = allocate_block(
                memory, m, n, blocks, active_ids, next_id
            )
            result.append(line)
            next_id = new_next_id

        elif op == "erase":
            x = int(parts[1])
            if x not in active_ids:
                result.append("ILLEGAL_ERASE_ARGUMENT")
            else:
                erase_block(blocks, memory, active_ids, x)

        elif op == "defragment":
            blocks = defragment_blocks(blocks, memory, m)

    return result


def print_results(result):
    for line in result:
        print(line)


def main():
    t, m = read_initial_parameters()
    result = simulate(t, m)
    print_results(result)


if __name__ == "__main__":
    main()
```

- Moved all executable logic into functions and added `main()` under `if __name__ == "__main__":` so nothing runs at import/top level.
- Split input, computation, and output into `read_initial_parameters`, `read_operation_parts`, `simulate`, and `print_results` for clearer separation of concerns.
- Replaced repeated memory-setting loops with the shared helper `set_memory_range`.
- Extracted allocation, erasure, and defragmentation behavior into dedicated helper functions while preserving the original mutation order and control flow.
- Kept all observable behavior, output ordering, and error propagation unchanged; only the internal structure was modified.