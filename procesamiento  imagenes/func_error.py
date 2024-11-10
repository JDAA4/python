import numpy as np

def binary_cross_entropy(y, y_pred):
    return -np.mean(y * np.log(y_pred) + (1 - y) * np.log(1 - y_pred))

def categorical_cross_entropy(y, y_pred):
    return -np.mean(y * np.log(y_pred))

y = np.array([1, 0, 1, 1, 0])
y_pred = np.array([0.9, 0.1, 0.8, 0.7, 0.2])

print("Entropia cruzada categorica",binary_cross_entropy(y, y_pred))
print("Entropia cruzada binaria",categorical_cross_entropy(y, y_pred))
