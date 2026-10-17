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


def find_first_fit(n):
    """Find the first contiguous free block of size n."""
    for i in range(1, m - n + 2):
        if all(not memory[j] for j in range(i, i + n)):
            return i
    return -1


def allocate_memory(n):
    """Allocate a block of size n and return its id, or None if no space."""
    global next_id
    pos = find_first_fit(n)
    if pos == -1:
        return None

    for i in range(pos, pos + n):
        memory[i] = True

    block_id = next_id
    blocks.append((block_id, pos, n))
    active_ids.add(block_id)
    next_id += 1
    return block_id


def erase_memory(block_id):
    """Free the memory associated with block_id. Return True if successful."""
    if block_id not in active_ids:
        return False

    for i, (b_id, start, length) in enumerate(blocks):
        if b_id == block_id:
            for j in range(start, start + length):
                memory[j] = False
            del blocks[i]
            active_ids.discard(block_id)
            return True
    return False


def defragment_memory():
    """Compact all allocated blocks to the beginning of memory."""
    global blocks
    blocks.sort(key=lambda b: b[1])

    current_pos = 1
    new_blocks = []
    for b_id, old_start, length in blocks:
        end_pos = current_pos + length - 1
        if end_pos > m:
            continue

        for i in range(old_start, old_start + length):
            memory[i] = False
        for i in range(current_pos, current_pos + length):
            memory[i] = True

        new_blocks.append((b_id, current_pos, length))
        current_pos += length

    blocks = new_blocks


for _ in range(t):
    parts = input().strip().split()
    op = parts[0]

    if op == "alloc":
        n = int(parts[1])
        block_id = allocate_memory(n)
        result.append(str(block_id) if block_id is not None else "NULL")

    elif op == "erase":
        x = int(parts[1])
        if not erase_memory(x):
            result.append("ILLEGAL_ERASE_ARGUMENT")

    elif op == "defragment":
        defragment_memory()

# Print results
for line in result:
    print(line)
