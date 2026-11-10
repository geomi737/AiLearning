import numpy as np


with open("aiheader.h", "w", encoding="UTF-8") as f:
    model = np.load("ai.npy")
    for layer_name, layer_items in model.items():
        layer_items: np.ndarray
        format_items = str(layer_items.tolist()).replace("[", "{").replace("]", "}")
        line = f"const float {layer_name}{f"[][{layer_items.shape[-1]}]" if layer_items.ndim ==
                                          2 else "[]"} PROGMEM = {format_items};"
        print(line, file=f)
        if layer_name[-1] == "w":
            line = f"const int {layer_name + "_rows"} = {len(layer_items)};"
            print(line, file=f)
            line = f"const int {layer_name + "_columns"} = {len(layer_items[0])};"
            print(line, file=f)