from __future__ import annotations
import numpy as np
from typing import List, Sequence
from .types import Detection

try:
    from tflite_runtime.interpreter import Interpreter  # type: ignore
except Exception:  # pragma: no cover
    from tensorflow.lite.python.interpreter import Interpreter  # type: ignore

class TFLiteObjectDetector:
    """Generic TFLite SSD-style object detector wrapper."""

    def __init__(self, model_path: str, labels: Sequence[str], score_threshold: float = 0.4):
        self.interpreter = Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.labels = list(labels)
        self.score_threshold = score_threshold

        in_details = self.interpreter.get_input_details()[0]
        self.input_index = in_details["index"]
        self.in_height = in_details["shape"][1]
        self.in_width = in_details["shape"][2]
        self.in_type = in_details["dtype"]

        out_details = self.interpreter.get_output_details()
        self.out_indices = [d["index"] for d in out_details]

    @staticmethod
    def _preprocess(frame_bgr: np.ndarray, w: int, h: int, dtype) -> np.ndarray:
        import cv2
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb, (w, h))
        x = np.expand_dims(resized, axis=0)
        if dtype == np.float32:
            x = x.astype(np.float32) / 255.0
        else:
            x = x.astype(dtype)
        return x

    def detect(self, frame_bgr: np.ndarray, max_results: int = 10) -> List[Detection]:
        x = self._preprocess(frame_bgr, self.in_width, self.in_height, self.in_type)
        self.interpreter.set_tensor(self.input_index, x)
        self.interpreter.invoke()

        out = [self.interpreter.get_tensor(i) for i in self.out_indices]

        boxes = out[0][0]  # (N,4) ymin,xmin,ymax,xmax
        classes = out[1][0].astype(int)
        scores = out[2][0]

        dets: List[Detection] = []
        for bbox, cls, score in zip(boxes, classes, scores):
            if float(score) < self.score_threshold:
                continue
            label = self.labels[cls] if 0 <= cls < len(self.labels) else f"class_{cls}"
            dets.append(Detection(label=label, score=float(score), bbox=tuple(map(float, bbox))))
            if len(dets) >= max_results:
                break
        return dets

def load_labels(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines()]
    return [ln for ln in lines if ln]
