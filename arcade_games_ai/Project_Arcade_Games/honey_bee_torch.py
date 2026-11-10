import torch
import torch.nn as nn
import torch.optim as optim

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Constants 
LEARNING_RATE = 0.0001
EPOCH = 100
BATCH = 256
FRAME_Q = -0.1
LOOSE_Q = -100
TUBE_Q = 1

# Model
expert = nn.Sequential(
    nn.Linear(3, 128),
    nn.ReLU(),
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Linear(64, 2)
).to(device)

learner = nn.Sequential(
    nn.Linear(3, 128),
    nn.ReLU(),
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Linear(64, 2)
).to(device)

# Optimizers
epsilone = 0.99
loss_function = nn.MSELoss()
optimizer = optim.AdamW(learner.parameters(), LEARNING_RATE)
