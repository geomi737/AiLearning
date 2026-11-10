import json
import numpy as np
import architecture as arc

with open("dataset.jsonl", "r", encoding="UTF-8") as dt:
    dataset = [json.loads(x) for x in dt.readlines()]

batch = 1024
epochs = 30
batched_dataset = [dataset[i:i + batch] for i in range(0, len(dataset) - batch, batch)]
LR = 1e-2

model = arc.MLP(
    arc.NeuralList([
        arc.NerualLayer(9, 36),
        arc.ReLU(),
        arc.NerualLayer(36, 18),
        arc.ReLU(),
        arc.NerualLayer(18, 9)
    ])
)
optimizer = arc.MSELoss(model, LR)

for epoch in range(1, epochs + 1):
    for batch in range(len(batched_dataset)):
        batch_data = batched_dataset[batch]
        inputs = np.array([np.array(x["situation"]).flatten() for x in batch_data])
        results = np.array([np.array(x["result_map"]).flatten() for x in batch_data])
        output = model(inputs)
        loss = optimizer(output, results)
        optimizer.backward()
        print(f"{epoch=}/{batch=}/{loss.item()=}")

with open("ai.npy", "wb") as f:
    np.savez(f,
             layer_1_w=model.layers[0].weights,
             layer_1_b=model.layers[0].biases,
             layer_2_w=model.layers[2].weights,
             layer_2_b=model.layers[2].biases,
             layer_3_w=model.layers[4].weights,
             layer_3_b=model.layers[4].biases
             )
