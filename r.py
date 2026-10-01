import os
import re
import pandas as pd
import numpy as np
from utils import convert_list
from main import ensure_file


def check(s: str) -> bool:
    s = s.replace(' ', '')
    return bool(re.fullmatch(r'[A-Za-z0-9]{4}', s))

def re_f(filepath):


    with open('res.txt', 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    df = pd.read_parquet(filepath)
    H, W = 40, 120

    new_image = []
    labels = []

    for idx, row in df.iterrows():

        label = lines[idx]
        if check(label):
            label = label.replace(' ', '').lower()
            flat_list = row["image"]
            new_image.append(convert_list(flat_list))
            labels.append(label)
    df = pd.DataFrame({
        "image": new_image,
        "labels": labels
    })

    df.to_parquet(f"new_{filepath}", engine="pyarrow", compression="zstd")


if __name__ == '__main__':
    p = ensure_file(
        './sichuan_gaokao.parquet',
        'xiaochuan-dev/captcha-new',
        'sichuan_gaokao.parquet'
    )
   
    re_f('sichuan_gaokao.parquet')