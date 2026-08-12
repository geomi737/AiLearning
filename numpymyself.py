import numpy as np


class Layer:
    def __init__(self, inputs: int, outputs: int) -> None:
        self.weights = np.reshape(np.random.randn(outputs), (outputs, 1))
        self.biases = np.reshape(np.zeros(outputs), (outputs, 1))

    def __call__(self, x: np.ndarray):
        logits = self.weights @ x.T + self.biases
        print(logits)


a = Layer(2, 4)
1 x 2                                                                                                                                                                                                                                                           
4 x 1

b = np.reshape(np.array([1, 2]), (2, 1))
a(b)
