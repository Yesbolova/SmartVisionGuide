import time

class CaneController:
    """Demo stub. Replace with BLE implementation later."""

    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True

    def vibrate(self, duration_ms: int):
        if not self.connected:
            print(f"[CANE] vibration {duration_ms} ms (not connected)")
            return
        print(f"[CANE] vibration {duration_ms} ms")
        time.sleep(duration_ms / 1000.0)
