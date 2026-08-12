from enum import Enum, auto
import torch
from torch import nn, optim
from torch.nn import functional as F
import os

class TS(Enum):
    TRAINING = auto()
    VALIDATING = auto()

os.chdir("./llmPractice")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

with open("Война и мир.txt", "r") as t:
    data = t.read()

# Embeddings
embedding_map = sorted(set(data))
itox = {value: key for key, value in enumerate(embedding_map)}
xtoi = {key: value for key, value in enumerate(embedding_map)}
encoder = lambda x: [itox[i] for i in x]
decoder = lambda x: "".join([xtoi[i] for i in x])

# Dataset
train_val_percentage = 90
n = int(len(data) * (train_val_percentage / 100))
training_data = torch.tensor(encoder(data[:n]))
val_data = torch.tensor(encoder(data[n:]))

# Settings
batch = 32
context = 16
epochs = 10000

def get_batch(part):
    data = training_data if part == TS.TRAINING else val_data
    icords = torch.randint(len(data) - context, (batch,))
    idx = torch.stack([data[starting_i:starting_i + context] for starting_i in icords])
    target = torch.stack([data[starting_i + 1:starting_i + context + 1] for starting_i in icords])

    return idx, target

class BiLM(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()

        self.embeddings = nn.Embedding(vocab_size, vocab_size)
    
    def forward(self, idx, target=None):
        # idx structure is (Batch, Time, Context)
        answer = self.embeddings(idx)
        if not target is None:
            b, t, c = answer.shape
            answer = torch.reshape(answer, (b * t, c))
            target = torch.reshape(target, (b * t,))
            loss = F.cross_entropy(answer, target)
        else:
            loss = None
        return answer, loss

    def generate(self, idx, token_amount):        
        for _ in range(token_amount):
            answer, loss = self(idx)
            answer = answer[:, -1, :]
            probabilities = F.softmax(answer, dim=-1)
            idx_next = torch.multinomial(probabilities, num_samples=1)
            idx = torch.cat((idx, idx_next), dim=1)
        return idx

model = BiLM(len(embedding_map))
optimizer = optim.AdamW(model.parameters())

for _ in range(epochs):
    idx, target = get_batch(TS.TRAINING)
    answer, loss = model(idx, target)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
print(decoder(model.generate(idx = torch.zeros((1, 1), dtype=torch.long), token_amount=500)[0].tolist()))
