import math
# Constants
MEM_SIZE = 2048
PAGE_SIZE = 16
# Memory
M = [None] * MEM_SIZE
# Swapping area
S = [None] * 4096
# To keep track of which frames every process is loaded at.
proc_pages = {}

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
    # The address of the frame where the page is stored.
    """ TODO: if the page is not loaded (it's in swapping area)
              it must be loaded by swapping-out a process.
    """
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
    # Pages left to load.
    pages_left = num_of_pages

    # Last frame where part of the process was loaded.
    last_frame = 0

    # Frames used.
    frames = []

    i = 0
    while pages_left > 0:

        # If there are no empty frames and
        # the process hasn't been loaded completely.
        if i >= MEM_SIZE and pages_left > 0:
            if(straregy):
                # FIFO
                print('fifo')
            else:
                # LRU
                print('lru')
            print()

        # Find first/next empty frame.
        while i < MEM_SIZE:
            if M[i] == None:
                frames.append(i)
                # Load to this frame.
                for j in range(0, PAGE_SIZE):
                    M[i + j] = p
                pages_left -= 1
                break
            # Move to next frame.
            i += PAGE_SIZE

    print("Se asignaron los marcos de página", frames, "al proceso", p)
    proc_pages[p] = frames

def L(p):

    print ("Liberar los marcos de página ocupados por el proceso ", p)
    
    if (proc_pages[p] == None): 
        print ("El proceso ", p, " no se ha ejecutado")
        return
    
    pages = proc_pages[p]
    size = len(pages) 
 
    for i in pages:
        for j in range(i, i + PAGE_SIZE):
            M[j] = None
   
    print ("Se liberan los marcos de página de memoria real: ", pages)

def E():
    print("Fin de las instrucciones")
    exit()