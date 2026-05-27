def process_and_search(original_list, target):
    # Step 1: Remove duplicates (set pattern)
    unique_list = list(set(original_list))   # set loses order, so sort after

    # Step 2: Sort (divide & conquer pattern – use merge sort)
    sorted_unique = merge_sort(unique_list)   # you implement merge_sort

    # Step 3: Search (binary search pattern)
    index = binary_search(sorted_unique, target)
    
    return index != -1   # True if found

# Helper functions (you must include these for the code to run)
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def binary_search(sorted_arr, target):
    left = 0
    right = len(sorted_arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if sorted_arr[mid] == target:
            return mid
        elif sorted_arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# --- Running the code ---
result = process_and_search([5, 2, 8, 2, 1], 8)
print(result)  # Output: True