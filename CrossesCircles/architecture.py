from functools import reduce
from typing import Any, Iterable
import numpy as np
import math


class Module:
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

    def backward(self, gradient: np.ndarray):
        pass


class NerualLayer(Module):
    def __init__(self, in_params: int, out_params: int) -> None:
        self.biases = np.zeros(out_params)
        self.weights = np.random.randn(in_params, out_params) * (math.sqrt(2 / in_params))

    def __call__(self, X: np.ndarray):
        self.activation = X
        return X @ self.weights + self.biases

    def backward(self, gradient: np.ndarray):
        deviation = self.activation.T @ gradient
        next_layer = gradient @ self.weights.T
        self.weights -= deviation
        self.biases -= np.sum(gradient, axis=0).flatten()
        return next_layer


class ReLU(Module):
    def __init__(self):
        pass

    def __call__(self, logits: np.ndarray) -> Any:
        self.activation = logits
        return np.maximum(0, logits)

    def backward(self, gradient: np.ndarray):
        gradient[self.activation < 0] = 0
        return gradient


class NeuralList(list):
    def __init__(self, iterable: Iterable) -> None:
        if not all(map(lambda x: isinstance(x, Module), iterable)):
            raise AttributeError("Not Module child classes in the iterable")
        super().__init__(iterable)


class MLP(Module):
    def __init__(self, iterable: NeuralList) -> None:
        self.layers = iterable

    def __call__(self, X: np.ndarray) -> Any:
        output = reduce(lambda logits, x: x(logits), self.layers, initial=X)
        return output

    def backward(self, gradient: np.ndarray) -> None:
        reduce(lambda gradient, x: x.backward(gradient), self.layers[::-1], initial=gradient)


class MSELoss:
    def __init__(self, model: Module, LR: float) -> None:
        self.model = model
        self.LR = LR

    def __call__(self, logits: np.ndarray, answer: np.ndarray) -> Any:
        self.logits, self.answer = logits, answer
        return np.average((logits - answer) ** 2)

    def backward(self):
        return self.model.backward(((2 / self.logits.size) * (self.logits - self.answer)) * self.LR)
