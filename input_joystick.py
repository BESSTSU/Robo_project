# input_joystick.py
# อ่านข้อมูลจาก Xbox One controller ผ่าน pygame
# แปลงแกนและปุ่มเป็นคำสั่งเดิน/เลี้ยว/ปรับความเร็ว/หยุด/ออก

import pygame
from input_base import InputDevice

class JoystickInput(InputDevice):
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            raise RuntimeError("ไม่พบจอยเชื่อมต่อ")
        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()

    def get_axes(self):
        pygame.event.pump()
        # แกนซ้ายแนวตั้ง (axis 1): บวก = ถอยหลัง, ลบ = เดินหน้า -> invert
        forward_back = -self.joy.get_axis(1)
        # แกนซ้ายแนวนอน (axis 0): บวก = เลี้ยวขวา, ลบ = เลี้ยวซ้าย
        turn = self.joy.get_axis(0)
        # deadzone เล็กน้อยเพื่อเลี่ยงสั่น
        if abs(forward_back) < 0.15:
            forward_back = 0.0
        if abs(turn) < 0.15:
            turn = 0.0
        return forward_back, turn

    def get_buttons(self):
        pygame.event.pump()
        # mapping ปุ่ม: RB=5 เพิ่มเร็ว, LB=4 ลดเร็ว, X=2 หยุด, Start=7 ออก
        return {
            "stop": bool(self.joy.get_button(2)),
            "exit": bool(self.joy.get_button(7)),
            "faster": bool(self.joy.get_button(5)),
            "slower": bool(self.joy.get_button(4)),
        }
