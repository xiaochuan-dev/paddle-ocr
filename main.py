import os
import pandas as pd
import numpy as np
from paddleocr import PaddleOCR
from huggingface_hub import hf_hub_download
from config import *
from utils import ensure_file


ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine="paddle",
    device="gpu",
)

def ocr_f(filepath):
    df = pd.read_parquet(filepath)

    for idx, row in df.iterrows():
        flat_list = row["image"]
        
        arr = np.array(flat_list, dtype=np.uint8).reshape(H, W, 3)

        # arr = np.array(flat_list, dtype=np.uint8).reshape(H, W)
        # arr = np.stack([arr, arr, arr], axis=-1)
        
        result = ocr.predict(arr)
        
        with open('res.txt', 'a+', encoding="utf-8") as f:
            for res in result:
                t = res["rec_texts"][0]
                f.write(f'{t}\n')

if __name__ == '__main__':
    p = ensure_file(
        'xinanjiaotong.parquet',
        'xiaochuan-dev/captcha-new',
        'xinanjiaotong.parquet'
    )
    ocr_f(p)