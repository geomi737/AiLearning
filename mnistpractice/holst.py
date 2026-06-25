import tkinter as tk
import math

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def click(event: tk.Event):
    x = math.floor(event.x / b)
    y = math.floor(event.y / b)
    if x >= standardsize or y >= standardsize or x <= -1 or y <= -1:
        return
    for xb in range(-1, 2):
        for yb in range(-1, 2):
            if (x + xb) < len(canvasmap) and (y + yb) < len(canvasmap):
                bias = 20 if xb == 0 and yb == 0 else 5 if xb != 0 and yb != 0 else 10
                canvasmap[y + yb][x + xb] += bias
                canvasmap[y + yb][x + xb] = 255 if canvasmap[y + yb][x + xb] > 255 else canvasmap[y + yb][x + xb]
                canvas.create_rectangle([(x + xb) * b, (y + yb) * b, (x + xb) * b + b, (y + yb) * b + b], fill=rgb_to_hex(*[int(canvasmap[y + yb][x + xb])] * 3), width=0)

def clear(event: tk.Event):
    global canvasmap 
    canvasmap = [
        [0 for _ in range(standardsize)] for _ in range(standardsize)
    ]
    canvas.delete("all")

root = tk.Tk()
b = 25
standardsize = 28
rootw = standardsize * b
rooty = standardsize * b
canvasmap = [
    [0 for _ in range(standardsize)] for _ in range(standardsize)
]
root.geometry(f"{rootw}x{rooty}")

canvas = tk.Canvas(root, background=rgb_to_hex(0, 0, 0))
canvas.pack(expand=1, fill="both")

root.bind("<B1-Motion>", click)
root.bind("<Button-3>", clear)

if __name__ == "__main__":
    root.mainloop()