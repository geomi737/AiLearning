import math
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
context = 64
epochs = 100
n_embed = 6500
head_num = 5
head_size = n_embed // head_num
n_layer = 5
mask = torch.triu(torch.ones(context, context), diagonal=1).bool()

def get_batch(part):
    data = training_data if part == TS.TRAINING else val_data
    icords = torch.randint(len(data) - context, (batch,))
    idx = torch.stack([data[starting_i:starting_i + context] for starting_i in icords])
    target = torch.stack([data[starting_i + 1:starting_i + context + 1] for starting_i in icords])

    return idx, target


class AttentionHead(nn.Module):
    def __init__(self):
        super().__init__()

        self.q = nn.Linear(n_embed, head_size, bias=False)
        self.k = nn.Linear(n_embed, head_size, bias=False)
        self.v = nn.Linear(n_embed, head_size, bias=False)
    
    def forward(self, x):
        qmap = self.q(x)
        kmap = self.k(x)
        vmap = self.v(x)
        qkmap = qmap @ torch.transpose(kmap, 1, 2) / math.sqrt(head_size)
        qkmap = torch.masked_fill(qkmap, mask, float("-inf"))
        value = F.softmax(qkmap, 2) @ vmap
        
        return value

class MultiHeadAttention(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.o = nn.Linear(n_embed, n_embed)
        self.heads = nn.ModuleList([AttentionHead() for _ in range(head_num)])

    def forward(self, x):
        x = self.o(torch.cat([head(x) for head in self.heads], dim=-1))
        return x

class Block(nn.Module):
    def __init__(self):
        self.MHA = MultiHeadAttention()
        self.MLP = nn.Sequential(
            nn.Linear(n_embed, n_embed * 4),
            nn.ReLU(),
            nn.Linear(n_embed * 4, n_embed)
        )

        self.lnmlp = nn.LayerNorm(n_embed)
        self.lnmha = nn.LayerNorm(n_embed)
    
    def forward(self, x):
        x = x + self.MHA(self.lnmha(x))
        x = x + self.mlp(self.lnmlp(x))

        return x

    
class Transformer(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()

        self.default_embeddings = nn.Embedding(vocab_size, n_embed)
        self.position_embeddings = nn.Embedding(context, n_embed)

        self.blocks = nn.Sequential(*[Block() for block in range(n_layer)])

        self.lntf = nn.LayerNorm(n_embed)
        self.lm_head = nn.Linear(n_embed, vocab_size)

    def forward(self, idx, target=None):
        # idx structure is (Batch, Tokens Of Batch, Data for each token)
        meaning = self.default_embeddings(idx)
        position = self.position_embeddings(idx)
        x = meaning + position

        x = self.blocks(x)
        x = self.lntf(x)
        x = self.lm_head(x)

        return x
        

model = Transformer(len(embedding_map))
optimizer = optim.AdamW(model.parameters())

print(decoder(model.generate(idx=torch.zeros((1, 1), dtype=torch.long), token_amount=1).tolist()[0]))
