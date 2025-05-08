from itertools import product
import stat

def generate_all_valid_sequences(max_len=10, num_colors=4):
    """Generate all valid sequences without consecutive duplicates."""
    sequences = set()
    for length in range(1, max_len + 1):
        for seq in product(range(1, num_colors + 1), repeat=length):
            # Keep only sequences without consecutive duplicates
            if all(seq[i] != seq[i+1] for i in range(len(seq)-1)):
                sequences.add(seq)
    return sorted(sequences)

# Print the sorted sequences
# for seq in sorted_sequences:
#     print(seq)


# def state_to_index(line,ball):
#         index = 0
#         for i,color in enumerate(line):
#             index += (color - 1) * (4**i)
#         index = (index * 4) + (ball-1)
#         return index

arr = generate_all_valid_sequences()

def state_to_index(line, ball,arr, sequences_dict=None):
    """Convert state to unique index."""
    if sequences_dict is None:
        # Generate lookup dictionary only once
        sequences = arr
        sequences_dict = {seq: i for i, seq in enumerate(sequences)}
    
    # Get base index for the line
    base_index = sequences_dict.get(tuple(line), 0)
    
    # Add ball color (0-3)
    return base_index * 4 + (ball - 1)

uniq = {}
flag = False
for i in arr:
    for j in range(1,5):
        index = state_to_index(i,j,arr)
        if index not in uniq:
            uniq[index] = (i,j)
            print("line: ", i, " ball: ", j , "index: ", index," ")
        else:
            print()
            print("not unique")
            print("line: ", i, " ball: ", j , "index: ", index)
            print("line: ", uniq[index][0], " ball: ", uniq[index][1], "index: ", index)
            flag = True
            break
    if flag:
        break
for i in range(118096 * 4):
    if i not in uniq:
        print("index: ", i, " not found")