# SmartVisionGuide (Sight+Guide)

AI-powered navigation prototype for visually impaired users: **smart glasses + mobile hub + adaptive cane feedback**.

## Why this project exists
Visually impaired people often struggle to detect obstacles and may rely on others for everyday navigation. The goal is to provide **real-time audio guidance** and **tactile cane signals** to support safer, more independent mobility.

## System concept (high level)
1. **Smart glasses / camera** capture the environment.
2. **AI engine** detects obstacles and estimates relative position.
3. **Mobile app (hub)** coordinates the feedback.
4. User receives:
   - **Audio guidance** (TTS)
   - **Tactile cues** for the cane (vibration patterns)

## What is in this repository
This repo is a *contest-friendly prototype scaffold*:
- A runnable **Python demo** (webcam → detection → danger scoring → TTS)
- Clear docs (user stories, architecture, ethics/privacy, demo script)
- A clean structure so you can extend it into:
  - mobile app (Flutter/Android)
  - wearable camera input
  - BLE cane integration

> Note: this template **does not ship a model**. You plug in any TFLite object-detection model you choose.

---

## Quick start (demo on laptop)
### 1) Create venv & install deps
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2) Provide a TFLite model + labels
Put files here:
- `models/model.tflite`
- `models/labels.txt`

Examples:
- SSD MobileNet v2 (TFLite)
- EfficientDet-Lite (TFLite)

### 3) Run
```bash
python -m src.main --model models/model.tflite --labels models/labels.txt
```

Keys:
- `q` — quit

---

## Folder structure
```
SmartVisionGuide/
  src/
    main.py
    detection/
      tflite_detector.py
      types.py
    guidance/
      danger.py
      tts.py
    cane/
      ble_stub.py
    io/
      video.py
  configs/
    default.json
  docs/
    architecture.md
    ethics_privacy.md
    user_stories.md
    demo_script.md
  models/              # (ignored by git by default)
  .gitignore
  requirements.txt
  LICENSE
```

---

## Credits & licensing
- This repository code is provided under **MIT** (see `LICENSE`).
- If you reuse external examples or models, keep their licenses and add credits in README.
