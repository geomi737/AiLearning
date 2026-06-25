from enum import Enum, auto
import torch
from torch import nn, optim
import os

class TS(Enum):
    TRAINING = auto()
    VALIDATING = auto()

os.chdir("./llmPractice")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

with open("Война и мир.txt", "r") as t:
    data = t.read()

# Dataset
train_val_percentage = 90
training_data = data[:int(len(data) * (train_val_percentage / 100))]
val_data = data[int(len(data) * (train_val_percentage / 100)):]

# Embeddings
embedding_map = sorted(set(data))
itox = {value: key for key, value in enumerate(embedding_map)}
xtoi = {key: value for key, value in enumerate(embedding_map)}
print(itox)
encoder = lambda x: [itox[i] for i in x]
decoder = lambda x: "".join([xtoi[i] for i in x])

# Settings
batch = 4
context = 8

def get_batch(part):
    data = training_data if part == TS.TRAINING else val_data
    ix = torch.randint(len(data) - context, (batch,))
    print(ix)
get_batch(TS.TRAINING)

class BiLM(nn.Module):
    def __init__(self):
        super.__init__()
    
    def forward(self, idx, target):
        # idx structure is (Batch, Time, C)
        pass