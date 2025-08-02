# input_base.py
# กำหนด interface พื้นฐานให้ input device ต่างๆ (เช่น joystick หรือ keyboard)
# เพื่อให้โค้ดส่วนกลางสามารถรับค่าแกน (forward/back, turn) และปุ่ม
# โดยไม่ต้องรู้ว่าได้มาจากแหล่งไหน

class InputDevice:
    def get_axes(self):
        """
        คืนค่า tuple (forward_back, turn) ในช่วง [-1, 1]
        forward_back: บวก = เดินหน้า, ลบ = ถอยหลัง
        turn: บวก = เลี้ยวขวา, ลบ = เลี้ยวซ้าย
        """
        raise NotImplementedError

    def get_buttons(self):
        """
        คืนค่า dict ของปุ่มสำคัญ เช่น:
        {
          'stop': False,
          'exit': False,
          'faster': False,
          'slower': False
        }
        """
        raise NotImplementedError
