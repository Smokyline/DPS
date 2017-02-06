from scipy.spatial.distance import cdist
import numpy as np

A = np.array([[1,0],[2,0]])
B = np.array([[10,0 ],[10, 0]])
print(A, B)
evk2 = cdist(A, B)
print(np.sum(evk2, axis=1))