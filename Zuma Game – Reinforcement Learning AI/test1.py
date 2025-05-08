def state_to_index(line,ball):
        index = 0
        for i,color in enumerate(line):
            index += (color) * (4**i)
        index = (index * 4) + (ball-1) - 4
        return index
    
from itertools import product
from math import e

from matplotlib.pyplot import flag

def generate_lines(max_length, num_colors):
    arr = []
    for length in range(1, max_length + 1):
        for combination in product(range(1, num_colors + 1), repeat=length):
            arr.append(list(combination))
    return arr

# Example usage
max_length = 9
num_colors = 4
arr = generate_lines(max_length, num_colors)
print("done creating lines")
uniq = {}
flag = False
for i in arr:
    for j in range(1,5):
        index = state_to_index(i,j)
        if index not in uniq:
            uniq[index] = (i,j)
        else:
            print()
            print("not unique")
            print("line: ", i, " ball: ", j , "index: ", index)
            print("line: ", uniq[index][0], " ball: ", uniq[index][1], "index: ", index)
            flag = True
            break
    if flag:
        break
else:
    print("unique")

for i in range(len(arr) * 4):
    if i not in uniq:
        print("index: ", i, " not found")