from numpy import uint8
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import holst as hst

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#Constants
LEARNING_RATE = 0.3
EPOCHS = 50
BATCH = 100
training_data = torch.from_numpy(np.fromfile("./mnistpractice/mnist-dataset/train-images.idx3-ubyte", dtype=uint8)[16:]).float().to(device) / 255
testing_data = torch.from_numpy(np.fromfile("./mnistpractice/mnist-dataset/t10k-images.idx3-ubyte", dtype=uint8)[16:]).float().to(device) / 255
training_answers = torch.from_numpy(np.fromfile("./mnistpractice/mnist-dataset/train-labels.idx1-ubyte", dtype=uint8)[8:]).to(device)
testing_answers = torch.from_numpy(np.fromfile("./mnistpractice/mnist-dataset/t10k-labels.idx1-ubyte", dtype=uint8)[8:]).to(device)

model = nn.Sequential(
    nn.Linear(28 * 28, 28 * 28),
    nn.ReLU(),
    nn.Linear(28 * 28, 28 * 28),
    nn.ReLU(),
    nn.Linear(28 * 28, 28 * 28),
    nn.ReLU(),
    nn.Linear(28 * 28, 10),
    nn.Softmax()
).to(device)

cost_function = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), LEARNING_RATE)

# Learning sequence
for epoch in range(1, EPOCHS + 1):
    for step in range(0, len(training_data), BATCH * 28 * 28):
        training_part = training_data[step:step + (BATCH * 28 * 28)].reshape(BATCH, 28 * 28)
        answer_part = training_answers[step // (28 * 28):step // (28 * 28) + BATCH]
        answer_one_hot = nn.functional.one_hot(answer_part.long(), 10).float()
        answer = model(training_part)
        loss = cost_function(answer, answer_one_hot)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    # Testing
    testing_answer = model(testing_data.reshape((len(testing_data) // (28 * 28), 28 * 28)))
    accuracy = torch.mean((torch.argmax(testing_answer, dim=1) == testing_answers).float()) * 100
    print(f"Эпоха: {epoch} | Потери: {loss.item():.4f} | Аккуратность {accuracy}%")

print("Тестирование")
def draw(event):
    answer = model((torch.tensor(hst.canvasmap).to(device) / 255).reshape(28 * 28))
    print(f"Вижу {torch.argmax(answer).item()}, уверен на {torch.max(torch.softmax(answer, 0)).item() * 100}%")

hst.root.bind("<ButtonRelease-1>", draw)
hst.root.mainloop()
