import torch

a = torch.tensor([
    [1, 2], 
    [2, 3], 
    [3, 4]])
b = torch.tensor([[4, 5], [5, 6], [6, 7]])
print(a @ b.T)