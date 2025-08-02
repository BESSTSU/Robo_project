from gpio_wrapper import GPIO

import time
import sys
import termios
import tty

# กำหนดพินของแต่ละมอเตอร์ (STEP, DIR)
PIN_CONFIG = {
    "FL": {"STEP": 13, "DIR": 21},
    "FR": {"STEP": 2,  "DIR": 3},
    "RL": {"STEP": 4,  "DIR": 7},
    "RR": {"STEP": 5,  "DIR": 6},
}

# ตั้งค่าทั่วไป
STEP_PULSE_WIDTH = 0.0005  # วินาที (500us) พัลส์สูง
DEFAULT_DELAY = 0.002      # delay ระหว่างสเต็ป -> ปรับเพื่อช้าหรือเร็ว

# กำหนดทิศทาง: True/False (จะกำหนดให้แต่ละมอเตอร์ตามการเรียกใช้)
DIR_FORWARD = GPIO.HIGH
DIR_BACKWARD = GPIO.LOW

# อ่าน key แบบไม่บล็อก
def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

class Stepper:
    def __init__(self, name, step_pin, dir_pin):
        self.name = name
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.output(self.step_pin, GPIO.LOW)
        GPIO.output(self.dir_pin, GPIO.LOW)

    def step(self, steps, direction, delay=DEFAULT_DELAY):
        GPIO.output(self.dir_pin, direction)
        for i in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(STEP_PULSE_WIDTH)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay - STEP_PULSE_WIDTH if delay > STEP_PULSE_WIDTH else 0)

    def set_direction(self, direction):
        GPIO.output(self.dir_pin, direction)

def move_all(steppers, direction_map, steps=200, delay=DEFAULT_DELAY):
    """
    direction_map: dict of motor_name -> direction (GPIO.HIGH/LOW)
    """
    # ตั้งทิศทางล่วงหน้า
    for name, stepper in steppers.items():
        dir_value = direction_map.get(name, DIR_FORWARD)
        stepper.set_direction(dir_value)
    # ทำสเต็ปพร้อมกัน (เรียงลูปให้ใกล้เคียงพร้อมกัน)
    for i in range(steps):
        for stepper in steppers.values():
            GPIO.output(stepper.step_pin, GPIO.HIGH)
        time.sleep(STEP_PULSE_WIDTH)
        for stepper in steppers.values():
            GPIO.output(stepper.step_pin, GPIO.LOW)
        time.sleep(delay - STEP_PULSE_WIDTH if delay > STEP_PULSE_WIDTH else 0)

def print_help():
    print("\nควบคุม Stepper Motors ผ่าน TB6600 (4 ตัว)")
    print("คำสั่ง:")
    print("  w : เดินหน้า")
    print("  s : ถอยหลัง")
    print("  a : เลี้ยวซ้าย")
    print("  d : เลี้ยวขวา")
    print("  x : หยุด/ไม่เคลื่อนที่ (แสดงว่าไม่มีสั่ง)")
    print("  + : เพิ่มความเร็ว (ลด delay)")
    print("  - : ลดความเร็ว (เพิ่ม delay)")
    print("  h : แสดง help")
    print("  q : ออก\n")
    print(f"ค่าความล่าช้า (delay ระหว่างสเต็ป): {DEFAULT_DELAY:.4f} วินาที (ปรับได้ด้วย +/-)\n")

def main():
    global DEFAULT_DELAY
    GPIO.setwarnings(False)

    # สร้างวัตถุมอเตอร์
    steppers = {}
    for name, pins in PIN_CONFIG.items():
        steppers[name] = Stepper(name, pins["STEP"], pins["DIR"])

    print_help()
    print("กดปุ่มเพื่อควบคุม (w/s/a/d), h เพื่อช่วยเหลือ, q เพื่อออก")

    try:
        while True:
            print(f"\nรอคำสั่ง (current delay={DEFAULT_DELAY:.4f}) > ", end="", flush=True)
            ch = getch()
            if ch == "q":
                print("\nออกจากโปรแกรม")
                break
            elif ch == "h":
                print_help()
            elif ch == "+":
                DEFAULT_DELAY = max(0.0005, DEFAULT_DELAY * 0.8)
                print(f"เพิ่มความเร็ว: delay ใหม่ = {DEFAULT_DELAY:.4f}")
            elif ch == "-":
                DEFAULT_DELAY = DEFAULT_DELAY * 1.25
                print(f"ลดความเร็ว: delay ใหม่ = {DEFAULT_DELAY:.4f}")
            elif ch == "w":
                # เดินหน้า: ทุกตัวไปทางเดียวกัน
                print("เคลื่อนที่: เดินหน้า")
                dir_map = {n: DIR_FORWARD for n in steppers}
                move_all(steppers, dir_map, steps=300, delay=DEFAULT_DELAY)
            elif ch == "s":
                print("เคลื่อนที่: ถอยหลัง")
                dir_map = {n: DIR_BACKWARD for n in steppers}
                move_all(steppers, dir_map, steps=300, delay=DEFAULT_DELAY)
            elif ch == "a":
                # เลี้ยวซ้าย: ซ้ายถอยหลัง ขวาเดินหน้า
                print("เคลื่อนที่: เลี้ยวซ้าย")
                dir_map = {
                    "FL": DIR_BACKWARD,
                    "RL": DIR_BACKWARD,
                    "FR": DIR_FORWARD,
                    "RR": DIR_FORWARD,
                }
                move_all(steppers, dir_map, steps=250, delay=DEFAULT_DELAY)
            elif ch == "d":
                # เลี้ยวขวา: ขวาถอยหลัง ซ้ายเดินหน้า
                print("เคลื่อนที่: เลี้ยวขวา")
                dir_map = {
                    "FL": DIR_FORWARD,
                    "RL": DIR_FORWARD,
                    "FR": DIR_BACKWARD,
                    "RR": DIR_BACKWARD,
                }
                move_all(steppers, dir_map, steps=250, delay=DEFAULT_DELAY)
            elif ch == "x":
                print("หยุด (ไม่มีการเคลื่อนที่)")
                # ไม่มีอะไรทำ
            else:
                print(f"ไม่รู้จักคำสั่ง '{ch}' (กด h ดู help)")
    except KeyboardInterrupt:
        print("\nรับสัญญาณหยุดจากผู้ใช้")
    finally:
        GPIO.cleanup()
        print("GPIO ถูกล้างแล้ว. จบโปรแกรม.")

if __name__ == "__main__":
    main()
