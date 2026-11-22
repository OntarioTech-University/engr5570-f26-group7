t, m = map(int, input().split())
memory = [False] * (m + 1)
blocks = []
next_id = 1
active_ids = set()
result = []
for _ in range(t):
    parts = input().strip().split()
    op = parts[-1]
    if op == 'alloc':
        n = int(parts[1])
        found = False
        pos = -1
        for i in range(1, m - n + 2):
            valid = True
            for j in range(i, i + n):
                if memory[j]:
                    valid = False
                    break
            if valid:
                pos = i
                found = True
                break
        if found:
            for i in range(pos, pos + n):
                memory[i] = True
            blocks.append((next_id, pos, n))
            active_ids.add(next_id)
            result.append(str(next_id))
            next_id += 1
        else:
            result.append('NULL')
    elif op == 'erase':
        x = int(parts[1])
        if x not in active_ids:
            result.append('ILLEGAL_ERASE_ARGUMENT')
        else:
            idx_to_remove = None
            for i in range(len(blocks)):
                b_id, start, length = blocks[i]
                if b_id == x:
                    idx_to_remove = i
                    for j in range(start, start + length):
                        memory[j] = False
                    break
            if idx_to_remove is not None:
                del blocks[idx_to_remove]
                active_ids.discard(x)
    elif op == 'defragment':
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
for line in result:
    print(line)
