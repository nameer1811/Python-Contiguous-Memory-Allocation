import sys
from random import randint

# default settings
settings = {"MEMORY_MAX" : 1024,
            "PROC_SIZE_MAX" : 512,
            "NUM_PROC" : 10,
            "MAX_PROC_TIME" : 10000}

# load in file
try:
    for l in open(sys.argv[1],"r"):
        flag_pos = [i for i, c in enumerate(l) if c == "<" or c == ">"]
        key = l[flag_pos[0]+1:flag_pos[1]]
        val = l[flag_pos[2]+1:flag_pos[3]]

        settings[key] = int(val)
except:
    print("Invalid File, using default variables")

MEMORY_MAX    = settings["MEMORY_MAX"]
PROC_SIZE_MAX = settings["PROC_SIZE_MAX"]
NUM_PROC      = settings["NUM_PROC"]
MAX_PROC_TIME = settings["MAX_PROC_TIME"]


# memory is a list of spaces available which merge
# memory start, memory size
avail_memory = [(0,MEMORY_MAX)]
working_processes = []

# method to allocate memory:
# first fit
def allocate(process):
    global avail_memory, working_processes, processes
    working_processes.append(process)
    process_size = process[1]
    allocated = False
    free_space = None

    # search for a spot to allocate this process
    for memory_chunk in avail_memory:
        if (memory_chunk[1]) >= process_size:
            allocated = True
            free_space  = memory_chunk

            # show allocation index
            process[0] = free_space[0]
            break

    # output an error if we cannot allocate
    if not allocated:
        proc_id = process[-1]
        print(f"error, cannot allocate space for process {proc_id}")
    else:
        processes.remove(process)
        # don't allocate the entire memory hole since the size of our request is smaller than it, record the new size of the memory hole 
        if free_space[1] > process_size:
            excess = (free_space[0]+process_size+1,free_space[1]-process_size)
            avail_memory.append(excess)

        avail_memory.remove(free_space)
        avail_memory.sort(key=lambda x : x[0])

def deallocate(process):
    global avail_memory, working_processes
    working_processes.remove(process)
    process_size = process[1]

    #memory_chunk = [m for m in avail if process[0] = m[0]]

    # deallocate this process
    new_memory = (process[0],process_size)
    avail_memory.append(new_memory)
    avail_memory.sort(key=lambda x : x[0])

    # then merge with potential other holes
    for i, memory_chunk in enumerate(avail_memory):
        if memory_chunk == new_memory:
            pos = i

    # merge left
    if pos-1 >= 0:
        left = avail_memory[pos-1]

        # they're right next to each other and can merge
        if left[0]+left[1] == process[0]-1:
            start = left[0]
            new_size = left[1]+process[1]
            avail_memory.remove(left)
            avail_memory.remove(new_memory)
            new_memory = (start,new_size)
            avail_memory.append(new_memory)
            avail_memory.sort(key=lambda x : x[0])

    # merge right
    if pos+1 < len(avail_memory):
        right = avail_memory[pos+1]

        # they're right next to each other and can merge
        if process[0]+process[1] == right[0]-1:
            start = process[0]
            new_size = right[1]+process[1]
            avail_memory.remove(right)
            avail_memory.remove(new_memory)
            new_memory = (start,new_size)
            avail_memory.append(new_memory)
            avail_memory.sort(key=lambda x : x[0])

# debug output to console of the memory
def print_memory():
    memory = avail_memory+working_processes

    # sort by start index
    memory.sort(key=lambda x : x[0])
    output = ""

    for memory_chunk in memory:
        # if it's a free space
        if len(memory_chunk) == 2:
            output += f"| Free ({memory_chunk[1]} KB)"
        else: # it's an allocated area, i.e. a process
            id = memory_chunk[-1]
            time = memory_chunk[2]
            output += f"| P{id} [{time}s] ()"

    print(output+" | ")


# print stats
def print_stats():
    total_size = sum([m[1] for m in avail_memory])
    avg_size = total_size/len(avail_memory)
    print("Number of memory holes:", len(avail_memory)-1)
    print("Average size of memory holes:", avg_size)
    print("Total memory free (size of current list of holes):",total_size)
    print("Memory free: ", str(round((total_size/MEMORY_MAX)*100))+"%")

# (allocation start, size, lifetime, id)
processes = [[-1,randint(0,PROC_SIZE_MAX),randint(0,MAX_PROC_TIME),id] for id in range(NUM_PROC)]

# service memory requests
print_memory()
print("Contiguous Memory Allocation Simulator")

while len(processes) != 0 and len(working_processes) != 0:
    print("----------------------------------------")
    for process in processes:
        allocate(process)

    for process in working_processes:
        # decrease amount of wait time
        if process[2] > 1:
            process[2] -= 1
        else:
            deallocate(process)

    print_memory()
    print_stats()

print("----------------------------------------")
print("Complete, all processes allocated succesfully")
print_memory()
print_stats()