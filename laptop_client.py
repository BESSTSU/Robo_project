import socket
import pygame
import time

# กำหนด IP และ PORT ของ Raspberry Pi
HOST = "192.168.166.237"  # แก้เป็น IP Pi จริง
PORT = 9000

# สปีดเริ่มต้น
speed = 80

def send_command(sock, cmd):
    print(f"ส่งคำสั่ง: {cmd}")
    sock.sendall((cmd + "\n").encode())

def main():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("ไม่พบจอย Xbox One กรุณาเชื่อมต่อก่อน")
        return

    joy = pygame.joystick.Joystick(0)
    joy.init()
    print(f"เชื่อมต่อจอย: {joy.get_name()}")

    sock = socket.create_connection((HOST, PORT))
    print(f"เชื่อมต่อ Raspberry Pi ที่ {HOST}:{PORT}")

    try:
        while True:
            pygame.event.pump()  # อัปเดตสถานะ joystick

            # อ่านแกนซ้าย: แกน 1 คือแกน Y ของสติ๊กซ้าย (-1 ดันขึ้น, +1 ดันลง)
            axis_y = joy.get_axis(1)
            axis_x = joy.get_axis(0)  # แกน X ซ้าย-ขวา

            # กำหนด deadzone เล็กน้อย
            deadzone = 0.2

            cmd = "S"  # ค่าเริ่มต้นคือหยุด

            # แปลงแกนเป็น speed %
            speed_pct = speed

            if abs(axis_y) > deadzone or abs(axis_x) > deadzone:
                if abs(axis_y) > abs(axis_x):
                    if axis_y < -deadzone:
                        cmd = f"F:{speed_pct}"  # เดินหน้า
                    elif axis_y > deadzone:
                        cmd = f"B:{speed_pct}"  # ถอยหลัง
                else:
                    if axis_x < -deadzone:
                        cmd = f"L:{speed_pct}"  # เลี้ยวซ้าย
                    elif axis_x > deadzone:
                        cmd = f"R:{speed_pct}"  # เลี้ยวขวา
            else:
                cmd = "S"  # หยุดถ้าไม่เอียงจอย

            send_command(sock, cmd)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("หยุดการทำงาน")

    finally:
        sock.close()
        pygame.quit()

if __name__ == "__main__":
    main()
