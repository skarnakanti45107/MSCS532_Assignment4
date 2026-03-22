import time
import random
import sys

# Increase recursion depth for Quicksort on reverse/sorted arrays to prevent crashes
sys.setrecursionlimit(100000)

# ==========================================
# 1. HEAPSORT IMPLEMENTATION
# ==========================================
def heapify(arr, n, i):
    """
    Maintains the max-heap property for a given subtree.
    """
    largest = i          # Initialize largest as root
    left = 2 * i + 1     # Left child index
    right = 2 * i + 2    # Right child index

    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Check if right child exists and is greater than the largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If the largest is not the root, swap and continue heapifying
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    """
    Main Heapsort function: builds a max-heap and extracts elements one by one.
    """
    n = len(arr)

    # Build a max-heap (rearrange array)
    # Start from the last non-leaf node and go up to the root
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements one by one from the heap
    for i in range(n - 1, 0, -1):
        # Move current root (maximum) to the end
        arr[i], arr[0] = arr[0], arr[i]
        # Call max heapify on the reduced heap
        heapify(arr, i, 0)

# ==========================================
# 2. ALGORITHMS FOR COMPARISON
# ==========================================
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort_wrapper(arr):
    quick_sort(arr, 0, len(arr) - 1)

# ==========================================
# 3. EMPIRICAL COMPARISON FRAMEWORK
# ==========================================
def generate_datasets(size):
    """Generates random, sorted, and reverse-sorted lists of a given size."""
    random_list = [random.randint(0, 100000) for _ in range(size)]
    sorted_list = sorted(random_list)
    reverse_sorted_list = sorted_list[::-1]
    return random_list, sorted_list, reverse_sorted_list

def measure_time(sort_func, data):
    """Measures the execution time of a sorting function."""
    arr_copy = data.copy()
    start_time = time.perf_counter()
    sort_func(arr_copy)
    end_time = time.perf_counter()
    return end_time - start_time

def run_experiment():
    sizes = [1000, 5000, 10000]
    algorithms = {
        "Heapsort": heap_sort,
        "Merge Sort": merge_sort,
        "Quicksort": quick_sort_wrapper
    }

    print("Empirical Comparison of Sorting Algorithms")
    print("-" * 65)
    print(f"{'Algorithm':<15} | {'Size':<6} | {'Random (s)':<12} | {'Sorted (s)':<12} | {'Reverse (s)':<12}")
    print("-" * 65)

    for size in sizes:
        random_list, sorted_list, reverse_list = generate_datasets(size)
        
        for name, func in algorithms.items():
            time_random = measure_time(func, random_list)
            
            # Note: Quicksort can hit maximum recursion depth or take excessively long 
            # on already sorted/reverse-sorted data due to O(n^2) worst case.
            time_sorted = measure_time(func, sorted_list)
            time_reverse = measure_time(func, reverse_list)

            print(f"{name:<15} | {size:<6} | {time_random:<12.5f} | {time_sorted:<12.5f} | {time_reverse:<12.5f}")

if __name__ == "__main__":
    run_experiment()