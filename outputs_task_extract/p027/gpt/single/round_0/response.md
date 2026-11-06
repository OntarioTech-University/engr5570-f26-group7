```python
def read_dimensions():
    return map(int, input().split())


def read_operation():
    parts = input().strip().split()
    return parts[0], parts


def is_free(start, length):
    for position in range(start, start + length):
        if memory[position]:
            return False
    return True


def find_first_fit(length):
    for position in range(1, m - length + 2):
        if is_free(position, length):
            return position
    return -1


def mark_memory(start, length, occupied):
    for position in range(start, start + length):
        memory[position] = occupied


def allocate(parts):
    global next_id

    length = int(parts[1])
    position = find_first_fit(length)
    if position == -1:
        result.append("NULL")
        return

    mark_memory(position, length, True)
    blocks.append((next_id, position, length))
    active_ids.add(next_id)
    result.append(str(next_id))
    next_id += 1


def find_block_index(block_id):
    for index in range(len(blocks)):
        if blocks[index][0] == block_id:
            return index
    return None


def erase(parts):
    block_id = int(parts[1])
    if block_id not in active_ids:
        result.append("ILLEGAL_ERASE_ARGUMENT")
        return

    index = find_block_index(block_id)
    if index is not None:
        _, start, length = blocks[index]
        mark_memory(start, length, False)
        del blocks[index]
        active_ids.discard(block_id)


def move_block(block, position):
    block_id, old_start, length = block
    end_position = position + length - 1
    if end_position > m:
        return None

    mark_memory(old_start, length, False)
    mark_memory(position, length, True)
    return block_id, position, length


def defragment():
    global blocks

    blocks.sort(key=lambda block: block[1])
    position = 1
    new_blocks = []
    for block in blocks:
        moved = move_block(block, position)
        if moved is not None:
            new_blocks.append(moved)
            position += block[2]
    blocks = new_blocks


def process_operation(op, parts):
    if op == "alloc":
        allocate(parts)
    elif op == "erase":
        erase(parts)
    elif op == "defragment":
        defragment()


def process_operations():
    for _ in range(t):
        op, parts = read_operation()
        process_operation(op, parts)


def print_results():
    for line in result:
        print(line)


t, m = read_dimensions()
memory = [False] * (m + 1)
blocks = []
next_id = 1
active_ids = set()
result = []

process_operations()
print_results()
```

- Separated input reading, operation dispatch, and output printing into dedicated functions.
- Split allocation, erasure, and defragmentation into small helpers while retaining their original processing order and behavior.