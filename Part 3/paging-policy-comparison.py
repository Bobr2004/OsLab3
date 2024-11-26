#! /usr/bin/env python3

import matplotlib.pyplot as plt

# FIFO Algorithm
def fifo_algorithm(pages, cachesize):
    cache = []
    page_faults = 0

    for page in pages:
        if page not in cache:
            page_faults += 1
            if len(cache) >= cachesize:
                cache.pop(0)  # Remove the oldest page
            cache.append(page)

    return page_faults

# LRU Algorithm
def lru_algorithm(pages, cachesize):
    cache = []
    page_faults = 0

    for page in pages:
        if page not in cache:
            page_faults += 1
            if len(cache) >= cachesize:
                cache.pop(0)  # Remove the least recently used page
        else:
            cache.remove(page)  # Move the page to the end
        cache.append(page)

    return page_faults

# WSClock Algorithm Helper
def wsclock_algorithm(new_page):
    global memory, clock_pointer, ref_bits, access_time, time_now, tau

    start_pointer = clock_pointer  # To check for a full cycle
    while True:
        candidate_page = memory[clock_pointer]

        # Check the reference bit
        if ref_bits[candidate_page] == 1:
            ref_bits[candidate_page] = 0  # Reset the reference bit
        else:
            # Check the last access time
            if time_now - access_time[candidate_page] > tau:
                # Replace the page
                del ref_bits[candidate_page]
                del access_time[candidate_page]
                memory[clock_pointer] = new_page
                ref_bits[new_page] = 1
                access_time[new_page] = time_now
                return  # Stop searching

        # Move to the next page
        clock_pointer = (clock_pointer + 1) % len(memory)

        # If we've returned to the starting position, replace without further checks
        if clock_pointer == start_pointer:
            victim_page = memory[clock_pointer]
            del ref_bits[victim_page]
            del access_time[victim_page]
            memory[clock_pointer] = new_page
            ref_bits[new_page] = 1
            access_time[new_page] = time_now
            return

# WSClock Simulation
def wsclock_simulation(pages, cachesize):
    global memory, clock_pointer, ref_bits, access_time, time_now, tau
    memory = []
    ref_bits = {}
    access_time = {}
    clock_pointer = 0
    tau = 10  # Aging time
    time_now = 0

    page_faults = 0

    for page in pages:
        time_now += 1  # Update the current time
        if page in memory:
            ref_bits[page] = 1  # Update the reference bit
            access_time[page] = time_now
        else:
            page_faults += 1
            if len(memory) >= cachesize:
                wsclock_algorithm(page)
            else:
                memory.append(page)
                ref_bits[page] = 1
                access_time[page] = time_now

    return page_faults

# Main Function for Comparison
if __name__ == "__main__":
    # Test data
    pages = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    cache_sizes = range(1, 6)

    # Results for each algorithm
    fifo_results = [fifo_algorithm(pages, size) for size in cache_sizes]
    lru_results = [lru_algorithm(pages, size) for size in cache_sizes]
    wsclock_results = [wsclock_simulation(pages, size) for size in cache_sizes]

    # Print results
    print("Page faults for different cache sizes:")
    print(f"FIFO: {fifo_results}")
    print(f"LRU: {lru_results}")
    print(f"WSClock: {wsclock_results}")

    # Plot the results
    plt.plot(cache_sizes, fifo_results, label="FIFO", marker='o')
    plt.plot(cache_sizes, lru_results, label="LRU", marker='s')
    plt.plot(cache_sizes, wsclock_results, label="WSClock", marker='^')
    plt.xlabel("Cache Size")
    plt.ylabel("Page Faults")
    plt.legend()
    plt.title("Comparison of Page Replacement Algorithms")
    plt.grid()
    plt.show()
