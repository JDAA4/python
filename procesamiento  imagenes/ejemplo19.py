import numpy as np

class Perceptron:

    def __init__(self, n_inputs, learning_rate=0.01):
        self.weights = np.random.rand(n_inputs )
        self.bias = 0
        self.learning_rate = learning_rate
    
    def predict(self, inputs):
            suma = np.dot(inputs, self.weights) + self.bias
            if suma > 0:
                return 1
            else:
                return 0
    
    def train(self, inputs, targets, n_epocas):
        for epocas in range(n_epocas):
            error = 0
            for i in range(len(inputs)):
                output = self.predict(inputs[i])
                delta = targets[i] - output
                self.weights += delta * self.learning_rate * inputs[i]
                self.bias += delta * self.learning_rate 
                error += delta
            if error == 0:
                print("Entrenamiento completado en la epoca: ", epocas)
                break

if __name__ == "__main__":
    inputs = np.array([[0, 0,0], [1,0,0], [0,1,0], [1,1,0],[0,0,1], [1,0,1], [1,1,1]])
    targets = np.array([0,0,0,0,0,0,1])
    
    mi_perceptron = Perceptron(3)
    mi_perceptron.train(inputs, targets, 100)
    for i in range(len(inputs)):
        output = mi_perceptron.predict(inputs[i])
        print(inputs[i], output)
