def read_input():
    return map(int, input().split())


def read_operation():
    return input().strip().split()


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


def mark_memory(memory, start, length, occupied):
    for i in range(start, start + length):
        memory[i] = occupied


def compute(t, m):
    # Memory representation: True means occupied; indexing is 1-based.
    memory = [False] * (m + 1)

    # Blocks are (id, start, length).
    blocks = []
    next_id = 1
    active_ids = set()
    result = []

    for _ in range(t):
        parts = read_operation()
        op = parts[0]

        if op == "alloc":
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

        elif op == "erase":
            x = int(parts[1])
            if x not in active_ids:
                result.append("ILLEGAL_ERASE_ARGUMENT")
            else:
                idx_to_remove = None
                for i in range(len(blocks)):
                    b_id, start, length = blocks[i]
                    if b_id == x:
                        idx_to_remove = i
                        mark_memory(memory, start, length, False)
                        break
                if idx_to_remove is not None:
                    del blocks[idx_to_remove]
                    active_ids.discard(x)

        elif op == "defragment":
            # Sort blocks by their current position to preserve order.
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
            blocks = new_blocks

    return result


def print_output(result):
    for line in result:
        print(line)


def main():
    t, m = read_input()
    result = compute(t, m)
    print_output(result)


if __name__ == "__main__":
    main()
