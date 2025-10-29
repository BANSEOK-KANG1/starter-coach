import os
from typing import Dict, Optional

import pandas as pd


def ensure_dir(path: str) -> str:
    """
    디렉터리가 없으면 생성하고, 최종 경로를 반환한다.
    """
    os.makedirs(path, exist_ok=True)
    return path


def append_log(file_path: str, row: Dict[str, object]) -> None:
    """
    단일 row(dict)를 CSV 로그 파일에 append한다.
    파일이 없으면 헤더 포함해서 새로 만든다.
    """
    # 처음 쓰는 경우에만 header를 쓴다
    write_header = not os.path.exists(file_path)

    df = pd.DataFrame([row])
    df.to_csv(
        file_path,
        mode="a",
        header=write_header,
        index=False,
        encoding="utf-8-sig",
    )


def read_logs(file_path: str) -> Optional[pd.DataFrame]:
    """
    CSV 로그 파일을 읽어 pandas DataFrame으로 반환.
    파일이 없거나 비어 있으면 None을 반환.
    """
    if not os.path.exists(file_path):
        return None

    try:
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    except Exception:
        return None

    if df.empty:
        return None

    # ts 컬럼(datetime) 파싱
    if "ts" in df.columns:
        df["ts"] = pd.to_datetime(df["ts"], errors="coerce")

    return df

