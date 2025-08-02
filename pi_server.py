import socket
import serial
import threading

# กำหนดพอร์ตรับจาก laptop
TCP_PORT = 9000
ESP_SERIAL = "/dev/ttyUSB0"  # ปรับตามที่ ESP32 ต่อ (ดูด้วย `ls /dev/tty*`)
BAUDRATE = 115200

def handle_client(conn, addr, esp):
    print(f"[TCP] เชื่อมต่อจาก {addr}")
    with conn:
        while True:
            data = conn.recv(64)
            if not data:
                break
            cmd = data.decode().strip()
            print(f"[TCP] ได้รับ: {cmd}")
            # ส่งต่อให้ ESP32
            esp.write((cmd + "\n").encode())
    print(f"[TCP] ตัดการเชื่อมต่อ {addr}")

def main():
    # เชื่อมต่อ ESP32 serial
    esp = serial.Serial(ESP_SERIAL, BAUDRATE, timeout=0.1)
    print(f"[Serial] เปิด {ESP_SERIAL} @ {BAUDRATE}")

    # สร้าง TCP server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", TCP_PORT))
        s.listen(1)
        print(f"[TCP] รอคอย client ที่พอร์ต {TCP_PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr, esp), daemon=True).start()

if __name__ == "__main__":
    main()
