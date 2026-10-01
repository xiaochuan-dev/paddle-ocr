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


def resize_keep_ratio_pad(
    img: Image.Image,
    target_h: int,
    target_w: int,
    fill: int = 255,
):

    src_w, src_h = img.size

    if src_w <= 0 or src_h <= 0:
        return Image.new("L", (target_w, target_h), fill)

    scale = min(
        target_w / src_w,
        target_h / src_h,
    )

    new_w = max(1, int(round(src_w * scale)))
    new_h = max(1, int(round(src_h * scale)))

    img = img.resize(
        (new_w, new_h),
        Image.Resampling.BILINEAR,
    )

    canvas = Image.new(
        "L",
        (target_w, target_h),
        fill,
    )

    offset_x = (target_w - new_w) // 2
    offset_y = (target_h - new_h) // 2

    canvas.paste(img, (offset_x, offset_y))

    return canvas

def convert_list(flat_list):
    width = 120
    height = 40

    arr = np.array(res, dtype=np.uint8).reshape(height, width)

    img = Image.fromarray(arr, mode="L")

    new_img = resize_keep_ratio_pad(img, 32, 128)
    return np.array(img, dtype=np.uint8).flatten().tolist()
