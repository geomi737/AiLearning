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
training_data = torch.tensor(encoder(data[:n]), device=device)
val_data = torch.tensor(encoder(data[n:]), device=device)

# Settings
batch = 32
context = 16
epochs = 1000
vocab = len(embedding_map)
n_embed = 32

def get_batch(part):
    data = training_data if part == TS.TRAINING else val_data
    icords = torch.randint(len(data) - context, (batch,)).to(device)
    idx = torch.stack([data[starting_i:starting_i + context] for starting_i in icords]).to(device)
    target = torch.stack([data[starting_i + 1:starting_i + context + 1] for starting_i in icords]).to(device)
    
    return idx, target

class BiLM(nn.Module):
    def __init__(self):
        super().__init__()

        self.token_embeddings = nn.Embedding(vocab, n_embed)
        self.position_embeddings = nn.Embedding(context, n_embed)
        self.lm_head = nn.Linear(n_embed, vocab)
    
    def forward(self, idx, target=None):
        # embed_token structure is (Batch, Tokens, Context)
        b, t = idx.shape

        token_embed = self.token_embeddings(idx)
        pos_embed = self.position_embeddings(torch.arange(t, device=device))
        
        x = token_embed + pos_embed
        
        logits = self.lm_head(x)
        b, t, c = logits.shape

        if not target is None:
            logits = torch.reshape(logits, (b * t, c))
            target = torch.reshape(target, (b * t,))
            loss = F.cross_entropy(logits, target)
        else:
            loss = None
        return logits, loss

    def generate(self, idx, token_amount):        
        for _ in range(token_amount):
            answer, loss = self(idx)
            answer = answer[:, -1, :]
            probabilities = F.softmax(answer, dim=-1)
            idx_next = torch.multinomial(probabilities, num_samples=1).to(device)
            idx = torch.cat((idx, idx_next), dim=1).to(device)
        return idx

model = BiLM().to(device)
optimizer = optim.AdamW(model.parameters())

for _ in range(epochs):
    idx, target = get_batch(TS.TRAINING)
    answer, loss = model(idx, target)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    if _ % 100 == 0:
        print(loss)

print(decoder(model.generate(idx = torch.tensor([[0]], device=device), token_amount=16)[0].tolist()))
