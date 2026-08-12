import torch

b = torch.tril(torch.ones((3, 4)))
a = torch.randint(0, 4, (4, 2)).float()
print(b, a, sep="\n")
c = b @ a
print(c)