def _is_free(memory, start, length):
    for index in range(start, start + length):
        if memory[index]:
            return False
    return True


def _find_first_fit(memory, m, length):
    for start in range(1, m - length + 2):
        if _is_free(memory, start, length):
            return start
    return None


def _mark_memory(memory, start, length):
    for index in range(start, start + length):
        memory[index] = True


def _clear_memory(memory, start, length):
    for index in range(start, start + length):
        memory[index] = False


def _handle_alloc(memory, m, length, blocks, active_ids, result, next_id):
    start = _find_first_fit(memory, m, length)

    if start is None:
        result.append("NULL")
        return next_id

    _mark_memory(memory, start, length)
    blocks.append((next_id, start, length))
    active_ids.add(next_id)
    result.append(str(next_id))

    return next_id + 1


def _handle_erase(memory, block_id, blocks, active_ids, result):
    if block_id not in active_ids:
        result.append("ILLEGAL_ERASE_ARGUMENT")
        return

    index_to_remove = None

    for index, (current_id, start, length) in enumerate(blocks):
        if current_id == block_id:
            index_to_remove = index
            _clear_memory(memory, start, length)
            break

    if index_to_remove is not None:
        del blocks[index_to_remove]
        active_ids.discard(block_id)


def _handle_defragment(memory, m, blocks):
    blocks.sort(key=lambda block: block[1])

    current_pos = 1
    defragmented_blocks = []

    for block_id, old_start, length in blocks:
        end_pos = current_pos + length - 1

        if end_pos > m:
            continue

        _clear_memory(memory, old_start, length)
        _mark_memory(memory, current_pos, length)
        defragmented_blocks.append((block_id, current_pos, length))
        current_pos += length

    return defragmented_blocks


t, m = map(int, input().split())

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
    parts = input().strip().split()
    op = parts[0]

    if op == "alloc":
        length = int(parts[1])
        next_id = _handle_alloc(
            memory, m, length, blocks, active_ids, result, next_id
        )
    elif op == "erase":
        block_id = int(parts[1])
        _handle_erase(memory, block_id, blocks, active_ids, result)
    elif op == "defragment":
        blocks = _handle_defragment(memory, m, blocks)

for line in result:
    print(line)
