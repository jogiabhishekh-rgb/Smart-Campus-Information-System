# Sorting and Searching Student IDs

student_ids = [105, 102, 110, 108, 101, 115]

print("Original IDs:", student_ids)

# Bubble Sort
n = len(student_ids)

for i in range(n):
    for j in range(0, n - i - 1):
        if student_ids[j] > student_ids[j + 1]:
            student_ids[j], student_ids[j + 1] = student_ids[j + 1], student_ids[j]

print("Sorted IDs:", student_ids)

target = int(input("Enter ID to search: "))

# Linear Search
found = False

for i in range(len(student_ids)):
    if student_ids[i] == target:
        print("Linear Search: Found at index", i)
        found = True
        break

if not found:
    print("Linear Search: Not Found")

# Binary Search
low = 0
high = len(student_ids) - 1

while low <= high:
    mid = (low + high) // 2

    if student_ids[mid] == target:
        print("Binary Search: Found at index", mid)
        break
    elif student_ids[mid] < target:
        low = mid + 1
    else:
        high = mid - 1
