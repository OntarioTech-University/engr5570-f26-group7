import sys

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
        if command == 'alloc':
            n = int(parts[1])
            found_pos = -1
            i = 0
            while i <= m - n:
                if memory[i] == 1:
                    j = i
                    while j < m and memory[j] == 0:
                        j += 1
                    if j - i >= n:
                        found_pos = i
                        break
                    else:
                        i = j
                else:
                    i += 1
            if found_pos != -1:
                print(next_id)
                active_ids.add(next_id)
                for k in range(found_pos, found_pos + n):
                    memory[k] = next_id
                next_id += 1
            else:
                print('NULL')
        elif command == 'erase':
            x = int(parts[1])
            if x > 0 and x in active_ids:
                active_ids.remove(x)
                for i in range(m):
                    if memory[i] == x:
                        memory[i] = 0
            else:
                print('ILLEGAL_ERASE_ARGUMENT')
        elif command == 'defragment':
            occupied_blocks = [block for block in memory if block != 0]
            memory = occupied_blocks + [0] * (m - len(occupied_blocks))
if __name__ == '__main__':
    memory_manager()
