# model/train.py
from pathlib import Path
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

def main():
    # ダミーデータ（2特徴量の二値分類）
    X = np.array([
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [1.0, 1.0],
    ])
    y = np.array([0, 0, 0, 1])

    model = LogisticRegression()
    model.fit(X, y)

    out = Path(__file__).resolve().parent / "model.joblib"
    joblib.dump(model, out)
    print(f"saved: {out}")

if __name__ == "__main__":
    main()
