ขั้นตอนใช้งาน

แฟลชโค้ด ESP32 ลงในบอร์ด (ผ่าน Arduino IDE หรือ VSCode)

เชื่อม ESP32 กับ TB6600 → Stepper

ต่อ ESP32 กับ Pi (USB หรือ UART TTL + level เหมาะสม)

รัน pi_server.py บน Raspberry Pi

        python3 pi_server.py

รัน laptop_client.py บน laptop (ปรับ IP ของ Pi)

กด w/s/a/d บน laptop เพื่อส่งคำสั่ง — โค้ดบน Pi จะส่งต่อให้ ESP32 ขับมอเตอร์
