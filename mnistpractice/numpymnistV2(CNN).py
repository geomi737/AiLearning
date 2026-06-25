from numpy import uint8
from functools import reduce
from dataclasses import dataclass
import numpy as np
import holst as hs

#Constants
batch = 150
learning_rate = 0.06
epochs = 100

#Dataset
padding_pattern = ((0, 0), (0, 0), (1, 1), (1, 1))
training_data = np.fromfile("./mnistpractice/mnist-dataset/train-images.idx3-ubyte", dtype=uint8)[16:].reshape(-1, 1, 28, 28) / 255
training_data = np.pad(training_data, padding_pattern, "constant", constant_values=0)

test_data = np.fromfile("./mnistpractice/mnist-dataset/t10k-images.idx3-ubyte", dtype=uint8)[16:].reshape(-1, 1, 28, 28) / 255
test_data = np.pad(test_data, padding_pattern, "constant", constant_values=0)

answers = np.fromfile("./mnistpractice/mnist-dataset/train-labels.idx1-ubyte", dtype=uint8)[8:]
test_answers = np.fromfile("./mnistpractice/mnist-dataset/t10k-labels.idx1-ubyte", dtype=uint8)[8:]

#Layers
class Conv2dLayer:
    def __init__(self, input_layers, core_amount):
        self.cores = np.random.randn()

class NeuralLayer:
    def __init__(self, input_layers, neuron_amount):
        self.weights = np.random.randn(input_layers, neuron_amount) * 0.1
        self.biases = np.zeros(neuron_amount)

    def forward(self, inputs):
        self.inputs = inputs
        #Calculating result
        self.neuron_result = inputs @ self.weights + self.biases
        #Applying RElU
        relu_result = np.maximum(0, self.neuron_result)
        return relu_result

    def backward(self, gradient):
        mask = (self.neuron_result > 0).astype(float)
        gradient *= mask

        backprop_gradient = gradient @ self.weights.T

        self.weights -= (self.inputs.T @ gradient) * learning_rate
        self.biases -= np.sum(gradient, axis=0) * learning_rate 
        return backprop_gradient

class ResponceLayer(NeuralLayer):
    def forward(self, inputs):
        self.inputs = inputs
        #Calculating result
        neuron_result = inputs @ self.weights + self.biases
        return neuron_result

    def backward(self, gradient):
        backprop_gradient = gradient @ self.weights.T
        # Калибруемся
        batch_size = gradient.shape
        self.weights -= (self.inputs.T @ gradient) * learning_rate
        self.biases -= np.sum(gradient, axis=0) * learning_rate
        return backprop_gradient

@dataclass
class Adapter:
    neural_list: list

    def calculate_output(self, data):
        return reduce(lambda acc, x: x.forward(acc), neural_list, data)
    
    def backprop(self, cost_gradient):
        reduce(lambda acc, x: x.backward(acc), neural_list[::-1], cost_gradient)

def zscore(inputs, mean=None, std=None):
    return inputs / 255

def cost(inputs, right_answer):
    return np.mean((inputs - right_answer) ** 2)  

def cost_backprop(inputs, right_answer):
    return (2 * (inputs - right_answer)) / batch

neural_list = [NeuralLayer(28 * 28, 128),
                 NeuralLayer(128, 64),
                  NeuralLayer(64, 32),
                  NeuralLayer(32, 16),
                ResponceLayer(16, 10)]
adapter = Adapter(neural_list)


# def make_prediction(event):
#     results = adapter.calculate_output(zscore(np.array(hs.canvasmap).reshape(1, 784), mean, std))
#     print(f"Это {np.argmax(results)}")


# hs.root.bind("<ButtonRelease-1>", make_prediction)
# hs.root.mainloop()
