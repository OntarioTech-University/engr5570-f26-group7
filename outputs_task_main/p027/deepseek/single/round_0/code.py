def read_input():
    t, m = map(int, input().split())
    operations = []
    for _ in range(t):
        parts = input().strip().split()
        op = parts[0]
        if op == "alloc":
            arg = int(parts[1])
        elif op == "erase":
            arg = int(parts[1])
        else:
            arg = None
        operations.append((op, arg))
    return t, m, operations


def set_memory_range(memory, start, length, value):
    for i in range(start, start + length):
        memory[i] = value


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


def find_block_index(blocks, block_id):
    for i, (b_id, start, length) in enumerate(blocks):
        if b_id == block_id:
            return i
    return None


def simulate(t, m, operations):
    memory = [False] * (m + 1)
    blocks = []
    next_id = 1
    active_ids = set()
    result = []

    for op, arg in operations:
        if op == "alloc":
            n = arg
            pos = find_first_fit(memory, m, n)
            if pos != -1:
                set_memory_range(memory, pos, n, True)
                blocks.append((next_id, pos, n))
                active_ids.add(next_id)
                result.append(str(next_id))
                next_id += 1
            else:
                result.append("NULL")

        elif op == "erase":
            x = arg
            if x not in active_ids:
                result.append("ILLEGAL_ERASE_ARGUMENT")
            else:
                idx_to_remove = find_block_index(blocks, x)
                if idx_to_remove is not None:
                    b_id, start, length = blocks[idx_to_remove]
                    set_memory_range(memory, start, length, False)
                    del blocks[idx_to_remove]
                    active_ids.discard(x)

        elif op == "defragment":
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
            blocks = new_blocks

    return result


def print_results(result):
    for line in result:
        print(line)


def main():
    t, m, operations = read_input()
    result = simulate(t, m, operations)
    print_results(result)


if __name__ == "__main__":
    main()
