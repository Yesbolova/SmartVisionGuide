from __future__ import annotations
import argparse
import json
import time

import cv2

from .io.video import open_camera
from .detection.tflite_detector import TFLiteObjectDetector, load_labels
from .guidance.danger import assess_hazard
from .guidance.tts import TTS
from .cane.ble_stub import CaneController

def load_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def draw_overlay(frame, detections):
    h, w = frame.shape[:2]
    for d in detections:
        ymin, xmin, ymax, xmax = d.bbox
        x1, y1 = int(xmin * w), int(ymin * h)
        x2, y2 = int(xmax * w), int(ymax * h)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
        cv2.putText(
            frame,
            f"{d.label} {d.score:.2f}",
            (x1, max(20, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/default.json")
    p.add_argument("--model", required=True, help="Path to .tflite model")
    p.add_argument("--labels", required=True, help="Path to labels.txt")
    return p.parse_args()

def main():
    args = parse_args()
    cfg = load_config(args.config)

    labels = load_labels(args.labels)
    detector = TFLiteObjectDetector(args.model, labels, score_threshold=cfg["score_threshold"])
    tts = TTS(enabled=cfg["tts"]["enabled"], rate=cfg["tts"]["rate"])
    cane = CaneController()
    cane.connect()

    cap = open_camera(cfg["camera_index"])
    cooldown_until = 0.0

    print("[INFO] Press 'q' to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        dets = detector.detect(frame, max_results=cfg["max_results"])

        hazard = assess_hazard(
            dets,
            near_area_ratio=cfg["danger"]["near_area_ratio"],
            medium_area_ratio=cfg["danger"]["medium_area_ratio"],
            near_vibration_ms=cfg["danger"]["near_vibration_ms"],
            medium_vibration_ms=cfg["danger"]["medium_vibration_ms"],
        )

        now = time.time()
        if hazard.level in ("near", "medium") and now >= cooldown_until:
            tts.say(hazard.message, cooldown_sec=cfg["danger"]["cooldown_sec"])
            cane.vibrate(hazard.vibration_ms)
            cooldown_until = now + cfg["danger"]["cooldown_sec"]

        draw_overlay(frame, dets)
        cv2.imshow("SmartVisionGuide - Demo", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
