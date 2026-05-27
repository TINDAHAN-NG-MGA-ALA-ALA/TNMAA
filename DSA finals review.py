def bubble_sort(arr):
    n = len(arr)
    for step in range(n - 1):
        swapped = False
        for i in range(n - step - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        
        if not swapped:
            break
            
    return arr

# --- Option 2: User input ---
# This part runs when the script starts
user_input = input("Enter numbers separated by spaces: ")
num_list = [int(x) for x in user_input.split()]
print(f"Sorted: {bubble_sort(num_list)}")