import sys

def memory_manager():
    """
    Implements a simple memory manager with alloc, erase, and defragment operations.
    """
    try:
        # Read the number of operations (t) and the total memory size (m)
        line = sys.stdin.readline()
        if not line:
            return
        t, m = map(int, line.split())
    except (IOError, ValueError):
        return

    # State of the memory manager
    memory = [0] * m  # 0 represents a free byte, a positive integer represents a block ID
    next_id = 1       # The ID for the next successful allocation
    active_ids = set() # A set of currently allocated (active) block IDs

    # Process each of the t operations
    for _ in range(t):
        line = sys.stdin.readline().strip()
        if not line:
            continue
        
        parts = line.split()
        command = parts[0]

        if command == "alloc":
            n = int(parts[1])
            
            # Find the first contiguous block of n free bytes (first-fit algorithm)
            # This search is optimized to be O(m)
            found_pos = -1
            i = 0
            while i <= m - n:
                if memory[i] == 0:
                    # Found a potential start of a free block. Check its length.
                    j = i
                    while j < m and memory[j] == 0:
                        j += 1
                    
                    # The length of the free block is (j - i)
                    if (j - i) >= n:
                        found_pos = i
                        break
                    else:
                        # This free block is too small. Jump past it to continue the search.
                        i = j
                else:
                    # This byte is occupied. Move to the next one.
                    i += 1
            
            if found_pos != -1:
                # A suitable block was found. Allocate it.
                print(next_id)
                active_ids.add(next_id)
                for k in range(found_pos, found_pos + n):
                    memory[k] = next_id
                next_id += 1
            else:
                # No suitable block could be found.
                print("NULL")

        elif command == "erase":
            x = int(parts[1])
            
            # Check if the provided ID is valid.
            # It must be a positive number and must correspond to a currently active block.
            if x > 0 and x in active_ids:
                # Valid ID. Proceed with erasing the block.
                active_ids.remove(x)
                # Iterate through memory and free the bytes belonging to this block.
                for i in range(m):
                    if memory[i] == x:
                        memory[i] = 0
            else:
                # Invalid ID. Report an error.
                print("ILLEGAL_ERASE_ARGUMENT")

        elif command == "defragment":
            # Compact the memory by moving all occupied blocks to the beginning.
            # The relative order of the blocks is preserved.
            
            # Create a new list containing only the occupied blocks.
            occupied_blocks = [block for block in memory if block != 0]
            # The new memory layout is the occupied blocks followed by free space.
            memory = occupied_blocks + [0] * (m - len(occupied_blocks))

# Run the memory manager simulation
if __name__ == "__main__":
    memory_manager()
