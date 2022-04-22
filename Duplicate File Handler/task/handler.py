import os
import sys
from collections import defaultdict

args = sys.argv
root_dir = ""
if len(args) != 2:
    print("Directory is not specified")
else:
    root_dir = args[1]

print("Enter file format:")
file_type = input()

print("Size sorting options:")
print("1. Descending")
print("2. Ascending")
print()

sorting_option = 0
print("Enter a sorting option:")
while True:
    sorting_option = int(input())
    if sorting_option <= 0 or sorting_option > 2:
        print("Wrong option")
    else:
        break
print()

file_list = defaultdict(list)

for path, currentDirectory, files in os.walk(root_dir):
    for file in files:
        if file_type != "" and file.endswith(f'.{file_type}'):
            file_list[os.stat(os.path.join(path, file)).st_size].append(os.path.join(path, file))
        elif file_type == "":
            file_list[os.stat(os.path.join(path, file)).st_size].append(os.path.join(path, file))

file_list_sorted = {}

if sorting_option == 1:
    file_list_sorted = sorted(file_list.items(), reverse=True)
else:
    file_list_sorted = sorted(file_list.items())

for key, values in file_list_sorted:
    print(f"{key} bytes")
    for v in values:
        print(v)
    print()