import gpiod

class GPIO:
    OUT = "out"
    HIGH = 1
    LOW = 0

    _chip = None
    _lines = {}

    @classmethod
    def _ensure_chip(cls):
        if cls._chip is None:
            try:
                cls._chip = gpiod.Chip('gpiochip0')
            except PermissionError:
                raise RuntimeError(
                    "ไม่สามารถเข้าถึง gpiochip0: ต้องรันด้วย sudo หรือเพิ่ม user ลงกลุ่ม gpio\n"
                    "เช่น: sudo usermod -aG gpio $(whoami) แล้ว logout/login หรือรัน `newgrp gpio`"
                )

    @classmethod
    def setwarnings(cls, flag):
        pass

    @classmethod
    def setmode(cls, mode):
        pass  # ไม่มีผล

    @classmethod
    def setup(cls, pin, direction):
        cls._ensure_chip()
        if pin in cls._lines:
            return
        line = cls._chip.get_line(pin)

        # เรียก request แบบเวอร์ชัน 1.6.3
        line.request(consumer="tb6600", type=gpiod.LINE_REQ_DIR_OUT)
        cls._lines[pin] = line

    @classmethod
    def output(cls, pin, value):
        if pin not in cls._lines:
            raise RuntimeError(f"GPIO {pin} ยังไม่ได้ setup")
        cls._lines[pin].set_value(1 if value else 0)

    @classmethod
    def cleanup(cls):
        for line in list(cls._lines.values()):
            try:
                line.release()
            except Exception:
                pass
        cls._lines.clear()
