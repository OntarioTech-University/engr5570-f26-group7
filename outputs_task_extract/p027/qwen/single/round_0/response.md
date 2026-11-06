```python
def read_initial_input():
    t, m = map(int, input().split())
    return t, m


def read_operation():
    return input().strip().split()


def initialize_state(m):
    # Memory representation: True means occupied
    memory = [False] * (m + 1)  # 1-based indexing
    blocks = []
    next_id = 1
    active_ids = set()
    result = []
    return memory, blocks, next_id, active_ids, result


def find_first_fit(memory, m, n):
    for i in range(1, m - n + 2):
        valid = True
        for j in range(i, i + n):
            if memory[j]:
                valid = False
                break
        if valid:
            return i
    return -1


def mark_memory(memory, start, length, value):
    for i in range(start, start + length):
        memory[i] = value


def allocate_memory(parts, m, memory, blocks, active_ids, result, next_id):
    n = int(parts[1])
    pos = find_first_fit(memory, m, n)
    if pos != -1:
        mark_memory(memory, pos, n, True)
        blocks.append((next_id, pos, n))
        active_ids.add(next_id)
        result.append(str(next_id))
        next_id += 1
    else:
        result.append("NULL")
    return next_id


def find_block(blocks, block_id):
    for i in range(len(blocks)):
        b_id, start, length = blocks[i]
        if b_id == block_id:
            return i, start, length
    return None, None, None


def erase_block(parts, memory, blocks, active_ids, result):
    x = int(parts[1])
    if x not in active_ids:
        result.append("ILLEGAL_ERASE_ARGUMENT")
        return

    idx_to_remove, start, length = find_block(blocks, x)
    if idx_to_remove is not None:
        mark_memory(memory, start, length, False)
        del blocks[idx_to_remove]
        active_ids.discard(x)


def defragment_blocks(blocks, memory, m):
    blocks.sort(key=lambda b: b[1])

    current_pos = 1
    new_blocks = []
    for b_id, old_start, length in blocks:
        end_pos = current_pos + length - 1
        if end_pos > m:
            continue

        mark_memory(memory, old_start, length, False)
        mark_memory(memory, current_pos, length, True)
        new_blocks.append((b_id, current_pos, length))
        current_pos += length

    return new_blocks


def process_operation(parts, m, memory, blocks, next_id, active_ids, result):
    op = parts[0]

    if op == "alloc":
        next_id = allocate_memory(
            parts, m, memory, blocks, active_ids, result, next_id
        )
    elif op == "erase":
        erase_block(parts, memory, blocks, active_ids, result)
    elif op == "defragment":
        blocks = defragment_blocks(blocks, memory, m)

    return blocks, next_id


def run_operations(t, m, memory, blocks, next_id, active_ids, result):
    for _ in range(t):
        parts = read_operation()
        blocks, next_id = process_operation(
            parts, m, memory, blocks, next_id, active_ids, result
        )


def print_results(result):
    for line in result:
        print(line)


def main():
    t, m = read_initial_input()
    memory, blocks, next_id, active_ids, result = initialize_state(m)

    run_operations(t, m, memory, blocks, next_id, active_ids, result)

    print_results(result)


if __name__ == "__main__":
    main()
```

- Extracted input reading into `read_initial_input` and `read_operation` so I/O is isolated from computation.
- Moved all initial state creation into `initialize_state` to keep setup explicit and testable.
- Split allocation logic into `find_first_fit`, `mark_memory`, and `allocate_memory`, each handling one responsibility.
- Split erase logic into `find_block` and `erase_block` to separate block lookup from state mutation.
- Moved defragmentation into `defragment_blocks` to isolate that computation step.
- Added `process_operation` and `run_operations` to keep the operation loop small and avoid top-level logic.
- Added `print_results` and a `main` entry point so the file has no long top-level execution block.
- Preserved the original control flow, output ordering, and error propagation without changing behavior.