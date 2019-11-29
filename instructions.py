import math
# Constants
MEM_SIZE = 2048
SWAP_MEM_SIZE = 4096
PAGE_SIZE = 16
STRATEGY = False # Will be revalued once main is run, for now it sets fifo as default
# Memory
M = [None] * MEM_SIZE
# Swapping area
S = [None] * SWAP_MEM_SIZE
# To keep track of which frames every process is loaded at.
""" 
    Structure:
    proc_pages = {
        "processId": {
            "Frame#": Space in real memory
        }

    }
"""
proc_pages = {}

# Track which frames of every process were swapped, and where they reside in the swapping memory
""" 
    Structure:
    swapped_pages = {
        "processId": {
            "Frame#": Space in swap memory
    }
"""
swapped_pages = {}

# Queue of pages used for FIFO Strategy
fifo_next_swap = []

# Queue of pages used for LRU Strategy
lru_next_swap = []

# Finds next available page in swap memory, and returns it
def findAvailableFrameInSwapMemory():
    for i in range(0,SWAP_MEM_SIZE,PAGE_SIZE):
        if(S[i]==None): return i

    print('La memoria de swap esta llena, se requiere más para completar la secuencia de procesos')
    print('Terminando ejecución por falta de memoria')
    exit()

# Loads page i with values val to memory
# i: page
# val: process or value to set
def loadPageToFrame(i, process, page):
    val = None if process == None and page == None else [process,page]
    for j in range(0, PAGE_SIZE):
        M[i + j] = val
            

# Loads page i with values val to swap memory
# i: page
# val: process or value to set
def loadPageToSwap(i, process, page):
    val = None if process == None and page == None else [process,page]
    for j in range(0, PAGE_SIZE):
        S[i + j] = val

# Puts the new process's new page into memory, in the next frame's current 
#  space of memory, and puts the current page in that frame into the swap area
# new_page: page number of the new frame
# new_process: process id of the new frame
# next_frame: space in memory that corresponds to where the new process will be placed
def swap(new_page, new_process, next_frame):
    # Get info of the previous process and its page at that space in memory
    [old_process, old_page] = M[next_frame]

    # Find next available frame in swap memory
    available_at_swap = findAvailableFrameInSwapMemory()

    # Load swapped page to swap memory
    loadPageToSwap(available_at_swap, old_process, old_page)

    # If process is not already in swapped_pages, add it
    if old_process not in swapped_pages:
        swapped_pages[old_process] = {}

    # Store in swapped_pages where the process will be stored in swap
    swapped_pages[old_process][old_page] = available_at_swap

    # Remove old frame from proc_pages
    del proc_pages[old_process][old_page]

    # Load page to the frame
    loadPageToFrame(next_frame, new_process, new_page)
    proc_pages[new_process][new_page] = next_frame

def chooseNext():
    # Choose which frame to use next
    if(STRATEGY):
        # FIFO
        # Get next frame to be swapped, and the process it corresponds to
        next_frame = fifo_next_swap.pop()
        # Add it back to queue, since it will be reused
        fifo_next_swap.insert(0, next_frame)
    else:
        # LRU
        # Get next frame to be swapped, and the process it corresponds to
        next_frame = lru_next_swap.pop()
        # Add it back to queue, since it will be reused
        lru_next_swap.insert(0, next_frame)
    return next_frame

# Updates an exsiting entry in the lru queue, placing it to the end of the queue
def updateLRU(page):
    lru_next_swap.remove(page)
    lru_next_swap.insert(0,page)
# Access virtual address "d" of process "p".
# d: virtual address (0 <= d <= max virtual address of "p")
# p: process ID
# m: mode (0 - read only, 1 - write)
def A(d, p, m):

    print("\nObtener la dirección real correspondiente a la dirección virtual", d, "del proceso", p, end="")
    if m == 1:
        print(" y modificar dicha dirección", end="")

    print("\nDirección virtual: ", d, ". ", end="", sep="")

    # Handle invalid cases
    if not p in proc_pages:
        print("\nError: no existe el proceso ", p, ".", sep="")
        return
    if d < 0 or d > len(proc_pages[p]) * PAGE_SIZE:
        print("\nError: la dirección virtual está fuera del rango de direcciones del proceso ", p, ".", sep="")
        return
    if m != 0 and m != 1:
        print("\nError: el modo de acceso debe ser 0 (lectura) o 1 (escritura).")
        return

    # Calculate the physical address.
    # The page number of the process (e.g. 0, 1, 2...)
    page = math.floor(d / PAGE_SIZE)
    # The displacement from the start of the page.
    fraction, whole = math.modf(d / PAGE_SIZE)
    disp = int(round(fraction, 4) * 16)
    
    if page not in proc_pages[p]:
        # page is in the swapping area
        # choose next frame to swap and swap it
        next_frame = chooseNext()        
        swap(page,p,next_frame)
        # Remove from this page from area
        page_in_swaparea = swapped_pages[p][page]
        loadPageToSwap(page_in_swaparea,None, None)
        del swapped_pages[p][page]
    elif not STRATEGY:
        # if the page is already in memory,and we are using lru
        # update lru queue to move the current page being
        updateLRU(proc_pages[p][page])
    # The address of the frame where the page is stored.
    frame = proc_pages[p][page]
    addr = frame + disp
    print("Dirección real:", addr)

# Load a process to memory (M).
# n: number of bytes (1 <= n <= 2048)
# p: process ID
# Command example: P 534 5834
def P(n, p):

    print("\nAsignar", n, "bytes al proceso", p)

    # Handle invalid cases
    if n <= 0:
        print("Error: el tamaño del proceso debe ser mayor que cero.")
        return

    if n > 2048:
        print("Error: el tamaño del proceso no puede exceder 2048 bytes.")
        return

    if p < 0:
        print("Error: el identificador del proceso debe ser igual o mayor que cero.")
        return

    if p in proc_pages:
        print("Error: ya existe un proceso con ese identificador.")
        return
    
    # Calculate how many pages are needed to load the process.
    num_of_pages = math.ceil(n / PAGE_SIZE)

    # Frames used.
    frames = []

    proc_pages[p] = {}
    i = 0
    current_page = 0
    while current_page < num_of_pages:

        # If there are no empty frames and
        # the process hasn't been loaded completely.
        if i >= MEM_SIZE and current_page < num_of_pages:
            
            next_frame = chooseNext()

            swap(current_page, p, next_frame)
            
            # Store loaded frame to display and store
            frames.append(next_frame)
            
            current_page += 1
            
            
        # Find first/next empty frame.
        while i < MEM_SIZE:
            if M[i] == None:
                # Store loaded frame to display and store
                frames.append(i)
                proc_pages[p][current_page] = i
                if(STRATEGY):
                    # If using fifo, add each used frame into the fifo queue
                    fifo_next_swap.insert(0, i)
                else:
                    # If using lru, add each frame into the lru queue 
                    lru_next_swap.insert(0, i)
                # Load to this frame.
                loadPageToFrame(i, p, current_page)
                current_page += 1
                break
            # Move to next frame.
            i += PAGE_SIZE

    print("Se asignaron los marcos de página", frames, "al proceso", p)

def L(p):

    print ("Liberar los marcos de página ocupados por el proceso ", p)
    if (proc_pages[p] == None):
        print ("El proceso ", p, " no se ha ejecutado")
        return

    # Frees up M
    pages = proc_pages[p]

    for key in pages:
        loadPageToFrame(pages[key],None, None)

    if STRATEGY:
        # Free up fifo queue of p's frames, only keeps frames that are not in the
        #  process being freed up
        fifo_next_swap = [i for i in fifo_next_swap if i not in pages.keys()]
    else:
        print("lru is not available yet")
        exit()

    del proc_pages[p]
    print ("Se liberan los marcos de página de memoria real: ", pages)

    # Frees up S

    if swapped_pages[p] != None :
        swapped = swapped[p]

        for key in swapped:
            loadPageToSwap(swapped[key], None, None)

        del swapped_pages[p]
        print ("Se liberan los marcos " , swapped, " del área de swapping")

def E():
    print("Fin de las instrucciones")
    exit()
"""   
P(2048,10)
A(50, 10, 0)

print(M)
print()
print(lru_next_swap)
"""