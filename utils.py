import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import ast

def show_rgb_image(H, W):
    with open('./a.txt', 'r') as f:
        image_str = f.read()
    pixels = ast.literal_eval(image_str)

    arr = np.array(pixels, dtype=np.uint8).reshape(H, W, 3)

    plt.figure(figsize=(12, 4))
    plt.imshow(arr)
    plt.axis("off")
    plt.show()