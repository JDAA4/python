import numpy as np
import matplotlib.pyplot as plt

def sigmoide(x):
    return 1 / (1 + np.exp(-x))

def step(x):
    return np.heaviside(x, 1)

def lineal(x):
    return x

def ReLU(x):
    return np.maximum(0, x)

def LeakyReLU(x,alpha=0.1):
    return np.maximum(alpha*x, x)

def tanh(x):
    return np.tanh(x)

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x))

x = np.linspace(-10, 10, 100)
y = softmax(x)
#y = [softmax(i) for i in x]
plt.plot(x, y)
plt.xlabel('Eje x')
plt.ylabel('Eje y')
plt.title('Función')
plt.grid(True)
plt.show()