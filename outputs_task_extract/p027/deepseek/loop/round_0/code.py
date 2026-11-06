def read_initial_counts():
    t, m = map(int, input().split())
    return t, m


def create_initial_state(m):
    return {
        'memory': [False] * (m + 1),
        'blocks': [],
        'next_id': 1,
        'active_ids': set(),
        'result': []
    }


def read_operation():
    return input().strip().split()


def process_operation(state, parts):
    op = parts[0]
    if op == "alloc":
        handle_alloc(state, int(parts[1]))
    elif op == "erase":
        handle_erase(state, int(parts[1]))
    elif op == "defragment":
        handle_defragment(state)


def handle_alloc(state, n):
    pos = find_first_fit(state['memory'], n, len(state['memory']) - 1)
    if pos == -1:
        state['result'].append("NULL")
    else:
        allocate_memory(state, pos, n)


def find_first_fit(memory, n, m):
    for i in range(1, m - n + 2):
        if is_range_free(memory, i, n):
            return i
    return -1


def is_range_free(memory, start, length):
    for j in range(start, start + length):
        if memory[j]:
            return False
    return True


def allocate_memory(state, pos, n):
    for i in range(pos, pos + n):
        state['memory'][i] = True
    block_id = state['next_id']
    state['blocks'].append((block_id, pos, n))
    state['active_ids'].add(block_id)
    state['result'].append(str(block_id))
    state['next_id'] += 1


def handle_erase(state, x):
    if x not in state['active_ids']:
        state['result'].append("ILLEGAL_ERASE_ARGUMENT")
    else:
        erase_block(state, x)


def erase_block(state, x):
    idx_to_remove = None
    for i, (b_id, start, length) in enumerate(state['blocks']):
        if b_id == x:
            idx_to_remove = i
            free_memory(state['memory'], start, length)
            break
    if idx_to_remove is not None:
        del state['blocks'][idx_to_remove]
        state['active_ids'].discard(x)


def free_memory(memory, start, length):
    for j in range(start, start + length):
        memory[j] = False


def handle_defragment(state):
    state['blocks'].sort(key=lambda b: b[1])
    current_pos = 1
    new_blocks = []
    for b_id, old_start, length in state['blocks']:
        end_pos = current_pos + length - 1
        if end_pos > len(state['memory']) - 1:
            continue
        free_memory(state['memory'], old_start, length)
        allocate_range(state['memory'], current_pos, length)
        new_blocks.append((b_id, current_pos, length))
        current_pos += length
    state['blocks'] = new_blocks


def allocate_range(memory, start, length):
    for i in range(start, start + length):
        memory[i] = True


def print_results(result):
    for line in result:
        print(line)


def main():
    t, m = read_initial_counts()
    state = create_initial_state(m)
    for _ in range(t):
        parts = read_operation()
        process_operation(state, parts)
    print_results(state['result'])


main()
