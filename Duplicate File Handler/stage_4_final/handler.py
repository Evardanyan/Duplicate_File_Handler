import os
import sys
import hashlib
from collections import defaultdict


def get_md5(file_path):
    m = hashlib.md5()
    with open(file_path, 'rb') as f:
        lines = f.read()
        m.update(lines)
    md5code = m.hexdigest()
    return md5code


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
file_list_hash = defaultdict(list)

for path, currentDirectory, files in os.walk(root_dir):
    for file in files:
        key = os.stat(os.path.join(path, file)).st_size
        value = os.path.join(path, file)
        if file_type != "" and file.endswith(f'.{file_type}'):
            file_list[key].append(value)
        elif file_type == "":
            file_list[key].append(value)

file_list_sorted = {}

if sorting_option == 1:
    file_list_sorted = dict(sorted(file_list.items(), reverse=True))
else:
    file_list_sorted = dict(sorted(file_list.items()))

file_list_sorted_merge_same_key = defaultdict(list)

for key1, val1 in file_list_sorted.items():
    for key2, val2 in file_list_sorted.items():
        if key1 == key2:
            if len(val2) > 1:
                for val3 in val2:
                    file_list_sorted_merge_same_key[key1].append(val3)

file_list_hash_sorted = defaultdict(list)
file_list_hash_sorted_double = defaultdict(list)
file_list_with_index = {}

for key, value in file_list_sorted_merge_same_key.items():
    for val in value:
        file_list_hash_sorted[get_md5(val)].append(val)

for key, value in file_list_hash_sorted.items():
    if len(value) > 1:
        for val in value:
            file_list_hash_sorted_double[key].append(val)

for key, values in file_list_sorted_merge_same_key.items():
    print(f"{key} bytes")
    for v in values:
        print(v)
    print()


def print_hash_info():
    global index
    index = 1
    temp_size = -1
    with open("myfile.txt", 'w') as f:
        for key, value in file_list_hash_sorted_double.items():
            f.write('%s:%s\n' % (key, value))
    for key, values in file_list_hash_sorted_double.items():
        file_size = os.stat(file_list_hash_sorted_double[key][0]).st_size
        if file_size != temp_size:
            print(f"{file_size} bytes")
            print(f"Hash: {key}")
        else:
            print(f"Hash: {key}")
        for v in values:
            print(f"{index}. {v}")
            file_list_with_index[index] = v
            # print(file_list_with_index)
            index = index + 1
        temp_size = file_size
        print()


def delete_files(files):
    total_bytes = 0
    for i in files:
        total_bytes = total_bytes + os.path.getsize(file_list_with_index[i])
        os.remove(file_list_with_index[i])
    print(f"Total freed up space: {total_bytes} bytes")


print("Check for duplicates?")
while (True):
    duplicate_check_input = input()
    print()
    if duplicate_check_input == "no":
        break
    elif duplicate_check_input == "yes":
        print_hash_info()
        break
    else:
        print("Wrong option")
        print("Check for duplicates?")

flag = True
print("Delete files?")
while flag:
    files_convert_int = []
    check = False
    delete_file = input()
    if delete_file == "no":
        break
    elif delete_file == "yes":
        while True:
            input_check = True
            while input_check:
                check_type = True
                while True:
                    input_delete_files_list = input()
                    if input_delete_files_list == "":
                        print("Wrong format")
                        print()
                        print("Enter file numbers to delete:")
                    else:
                        break
                files = input_delete_files_list.split()
                for i in files:
                    try:
                        int(i)
                    except ValueError:
                        check_type = False
                        print("Wrong format")
                        print()
                        print("Enter file numbers to delete:")
                        continue
                if check_type is True:
                    input_check = False
            files_convert_int = [int(x) for x in files]
            for i in files_convert_int:
                if i > index:
                    print("Wrong format")
                    print()
                    print("Enter file numbers to delete:")
                    break
            delete_files(files_convert_int)
            flag = False
            break
    else:
        print("Wrong format")
        print("Enter file numbers to delete:")
