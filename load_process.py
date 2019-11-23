import math

# Constants
MEM_SIZE = 2048
PAGE_SIZE = 16
# Memory
M = [None] * MEM_SIZE
# Swapping area
S = [None] * 4096
# To keep track of which pages every process is loaded at.
proc_pages = {}

# Load a process to memory (M).
# n: number of bytes (1 <= n <= 2048)
# p: process ID
# Command example: P 534 5834
def load_process(n, p):

    print("Asignar ", n, " bytes al proceso ", p)

    # Calculate how many pages are needed to load the process.
    pages = math.ceil(n / PAGE_SIZE)
    if pages <= 0:
        print("Error: process size must be positive")
        return

    if p < 0:
        print("Error: process ID must be zero or positive")
        return
    
    # Pages left to load.
    pages_left = pages
    # Last page where part of the process was loaded.
    last_page = 0

    # Pages used.
    pages = []

    while pages_left > 0:
        # Find first empty page from the last page loaded.
        i = last_page
        while i < MEM_SIZE:
            last_page = i + PAGE_SIZE
            if M[i] == None:
                pages.append(i)
                # Load to this page.
                for j in range(0, PAGE_SIZE):
                    M[i + j] = p
                pages_left -= 1
                break

    print("Se asignaron los marcos de página ", pages, " al proceso ", p)
    proc_pages[p] = pages

