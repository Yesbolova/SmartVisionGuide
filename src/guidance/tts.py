import time
from typing import Optional

try:
    import pyttsx3
except Exception:  # pragma: no cover
    pyttsx3 = None

class TTS:
    def __init__(self, enabled: bool = True, rate: int = 170):
        self.enabled = enabled and (pyttsx3 is not None)
        self._engine = None
        self._cooldown_until = 0.0
        self._last_text: Optional[str] = None

        if self.enabled:
            self._engine = pyttsx3.init()
            self._engine.setProperty("rate", rate)

    def say(self, text: str, cooldown_sec: float = 1.2):
        if not self.enabled:
            return
        now = time.time()
        if now < self._cooldown_until:
            return
        if self._last_text == text:
            return

        self._cooldown_until = now + cooldown_sec
        self._last_text = text
        assert self._engine is not None
        self._engine.say(text)
        self._engine.runAndWait()
