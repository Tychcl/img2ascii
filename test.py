import numpy as np

arr = np.array([-1, 0, 1, 2, 3, 4, 0, 0, 1, 2, 2, -1, 4, 4, 4])

print(np.unique(arr, return_counts=True)[1][1:])