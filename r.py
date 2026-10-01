import os
import pandas as pd
import numpy as np

def re():


    with open('res.txt', 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    print(lines)
    df = pd.read_parquet(filepath)
    H, W = 40, 120

    new_image = []
    labels = []

    for idx, row in df.iterrows():
        flat_list = row["image"]

if __name__ == '__main__':
   
    re()