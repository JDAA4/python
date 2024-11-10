import numpy as np
bias1 = 2
bias2 = 3
bias3 = 0.5
inputs = [1,1,2,3,2.5]
weights1 = [bias1,0.2, 0.8, -0.5, 1]
weights2 = [bias2,0.5, -0.91, 0.26, -0.5]
weights3 = [bias3,-0.26, -0.27, 0.17, 0.87]
output =[np.dot(inputs, weights1), np.dot(inputs, weights2) , np.dot(inputs, weights3) ]

print(output)