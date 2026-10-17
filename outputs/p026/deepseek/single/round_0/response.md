```python
import sys


def read_initial_parameters():
    """
    Read the number of operations and total memory size from stdin.
    
    Returns:
        tuple: (t, m) where t is the number of operations and m is the memory size.
        None: if input is invalid or missing.
    """
    try:
        line = sys.stdin.readline()
        if not line:
            return None
        return tuple(map(int, line.split()))
    except (IOError, ValueError):
        return None


def find_first_fit(memory, size_needed):
    """
    Find the first contiguous block of free bytes using the first-fit algorithm.
    
    Args:
        memory: List representing memory state (0 = free, positive integer = block ID).
        size_needed: Number of contiguous free bytes required.
    
    Returns:
        int: Starting index of the found block, or -1 if no suitable block exists.
    """
    m = len(memory)
    i = 0
    
    while i <= m - size_needed:
        if memory[i] == 0:
            # Found a potential start of a free block. Check its length.
            j = i
            while j < m and memory[j] == 0:
                j += 1
            
            if (j - i) >= size_needed:
                return i
            # This free block is too small. Jump past it to continue the search.
            i = j
        else:
            # This byte is occupied. Move to the next one.
            i += 1
    
    return -1


def allocate_memory(memory, next_id, active_ids, size):
    """
    Attempt to allocate a block of memory.
    
    Args:
        memory: List representing memory state.
        next_id: The next block ID to assign.
        active_ids: Set of currently active block IDs.
        size: Size of the block to allocate.
    
    Returns:
        tuple: (memory, next_id, active_ids) after the allocation attempt.
    """
    found_pos = find_first_fit(memory, size)
    
    if found_pos != -1:
        print(next_id)
        active_ids.add(next_id)
        for k in range(found_pos, found_pos + size):
            memory[k] = next_id
        next_id += 1
    else:
        print("NULL")
    
    return memory, next_id, active_ids


def erase_memory(memory, active_ids, block_id):
    """
    Attempt to erase a block of memory.
    
    Args:
        memory: List representing memory state.
        active_ids: Set of currently active block IDs.
        block_id: The ID of the block to erase.
    
    Returns:
        list: Updated memory state after the erase attempt.
    """
    if block_id > 0 and block_id in active_ids:
        active_ids.remove(block_id)
        for i in range(len(memory)):
            if memory[i] == block_id:
                memory[i] = 0
    else:
        print("ILLEGAL_ERASE_ARGUMENT")
    
    return memory


def defragment_memory(memory):
    """
    Compact memory by moving all occupied blocks to the beginning.
    
    Args:
        memory: List representing memory state.
    
    Returns:
        list: Defragmented memory state.
    """
    occupied_blocks = [block for block in memory if block != 0]
    return occupied_blocks + [0] * (len(memory) - len(occupied_blocks))


def process_operation(memory, next_id, active_ids, line):
    """
    Process a single memory management operation.
    
    Args:
        memory: List representing memory state.
        next_id: The next block ID to assign.
        active_ids: Set of currently active block IDs.
        line: The operation line to process.
    
    Returns:
        tuple: (memory, next_id, active_ids) after processing the operation.
    """
    parts = line.split()
    command = parts[0]
    
    if command == "alloc":
        size = int(parts[1])
        memory, next_id, active_ids = allocate_memory(memory, next_id, active_ids, size)
    elif command == "erase":
        block_id = int(parts[1])
        memory = erase_memory(memory, active_ids, block_id)
    elif command == "defragment":
        memory = defragment_memory(memory)
    
    return memory, next_id, active_ids


def memory_manager():
    """
    Implements a simple memory manager with alloc, erase, and defragment operations.
    """
    params = read_initial_parameters()
    if params is None:
        return
    
    t, m = params
    
    # State of the memory manager
    memory = [0] * m  # 0 represents a free byte, a positive integer represents a block ID
    next_id = 1       # The ID for the next successful allocation
    active_ids = set()  # A set of currently allocated (active) block IDs
    
    # Process each of the t operations
    for _ in range(t):
        line = sys.stdin.readline().strip()
        if not line:
            continue
        
        memory, next_id, active_ids = process_operation(memory, next_id, active_ids, line)


# Run the memory manager simulation
if __name__ == "__main__":
    memory_manager()
```

**Summary of changes:**

- **Extracted `read_initial_parameters()`**: Separated input parsing logic from the main function to improve readability and error handling clarity.
- **Extracted `find_first_fit()`**: Moved the first-fit allocation search algorithm into its own function, making the allocation logic cleaner and the search algorithm independently testable.
- **Extracted `allocate_memory()`**: Encapsulated the allocation operation, reducing complexity in the main loop and making the operation's intent clearer.
- **Extracted `erase_memory()`**: Separated the erase operation logic, simplifying the main loop and making the validation and memory clearing steps more readable.
- **Extracted `defragment_memory()`**: Moved the defragmentation logic into a dedicated function, making the operation self-contained and easier to understand.
- **Extracted `process_operation()`**: Created a dispatcher function that handles command routing, reducing the main loop's complexity and making it easier to add new operations in the future.
- **Simplified main loop**: The `memory_manager()` function now focuses on orchestration rather than implementation details, improving overall readability and maintainability.