# Architecture

Pipeline:
1) Camera input (smart glasses / webcam)
2) AI detection (TFLite object detection model)
3) Hazard scoring (heuristics / future ML)
4) Feedback:
   - Text-to-Speech (audio)
   - Cane controller (vibration patterns; demo stub)

Data flow: Frame -> Detector -> Detections -> Hazard -> (TTS + Cane)
