import os
import pandas as pd
import numpy as np
from paddleocr import PaddleOCR
from huggingface_hub import hf_hub_download

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

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine="paddle",
)

def ocr_f(filepath):
    df = pd.read_parquet(filepath)
    H, W = 40, 120

    for idx, row in df.iterrows():
        flat_list = row["image"]
        
        # arr = np.array(flat_list, dtype=np.uint8).reshape(H, W, 3)

        arr = np.array(flat_list, dtype=np.uint8).reshape(H, W)
        arr = np.stack([arr, arr, arr], axis=-1)
        
        result = ocr.predict(arr)
        
        with open('res.txt', 'w+', encoding="utf-8") as f:
            for res in result:
                t = res["rec_texts"][0]
                f.write(f'{t}\n')

if __name__ == '__main__':
    p = ensure_file(
        './sichuan_gaokao.parquet',
        'xiaochuan-dev/captcha-new',
        'sichuan_gaokao.parquet'
    )
    ocr_f(p)