from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
from ..detection.types import Detection

@dataclass(frozen=True)
class Hazard:
    level: str  # "near" | "medium" | "none"
    message: str
    vibration_ms: int

def bbox_area_ratio(bbox: Tuple[float, float, float, float]) -> float:
    ymin, xmin, ymax, xmax = bbox
    w = max(0.0, xmax - xmin)
    h = max(0.0, ymax - ymin)
    return w * h

def assess_hazard(
    detections: List[Detection],
    near_area_ratio: float = 0.12,
    medium_area_ratio: float = 0.06,
    near_vibration_ms: int = 450,
    medium_vibration_ms: int = 250,
) -> Hazard:
    """Distance heuristic via bbox area ratio (bigger box => closer)."""
    if not detections:
        return Hazard(level="none", message="", vibration_ms=0)

    best = max(detections, key=lambda d: bbox_area_ratio(d.bbox))
    area = bbox_area_ratio(best.bbox)

    if area >= near_area_ratio:
        return Hazard(level="near", message=f"Obstacle very close: {best.label}", vibration_ms=near_vibration_ms)
    if area >= medium_area_ratio:
        return Hazard(level="medium", message=f"Obstacle ahead: {best.label}", vibration_ms=medium_vibration_ms)

    return Hazard(level="none", message="", vibration_ms=0)
