import pickle
import numpy as np
files = ["q_table10Mr10fix_vector"]
# files = ["q_table100m"]
vector = None
q_table = None
for file in files:
    with open(file + ".pkl", 'rb') as f:
        data = pickle.load(f)
        q_table = data.q_table
        vector = np.zeros(q_table.shape[0], dtype=np.uint8)
        for i in range(q_table.shape[0]):
            vector[i] = np.argmax(q_table[i, :])
    np.savez_compressed(file + "bit", q_table=vector)
    print("done", file)
        