import os
THRESHOLD = int(os.getenv("THRESHOLD", 10))
def predict_logic(x: int) -> int:
    if x > THRESHOLD:
        return 1
    return 0
