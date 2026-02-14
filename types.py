from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Detection:
    label: str
    score: float
    # bounding box in normalized coordinates: (ymin, xmin, ymax, xmax) in [0,1]
    bbox: Tuple[float, float, float, float]
