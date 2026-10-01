import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import ast

def ensure_file(
    local_path: str,
    repo_id: str,
    filename: str,
) -> str:
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        print(f"使用本地数据: {local_path}", flush=True)
        return local_path

    print(f"本地未找到 {local_path}", flush=True)
    print(f"正在从 Hugging Face 下载: {filename}", flush=True)
    print(f"  repo: {repo_id}", flush=True)

    os.makedirs(os.path.dirname(local_path) or ".", exist_ok=True)

    downloaded = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        repo_type="dataset",
        local_dir=os.path.dirname(os.path.abspath(local_path)) or ".",
    )

    if os.path.abspath(downloaded) != os.path.abspath(local_path):
        if not os.path.exists(local_path):
            os.replace(downloaded, local_path)

    print(f"下载完成: {local_path}", flush=True)
    return local_path


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
