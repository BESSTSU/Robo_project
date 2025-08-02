#include <Arduino.h>

// กำหนดพินสำหรับ TB6600 (ปรับตามการต่อจริง)
#define FL_STEP 5
#define FL_DIR  18
#define FR_STEP 19
#define FR_DIR  21
#define RL_STEP 22
#define RL_DIR  23
#define RR_STEP 25
#define RR_DIR  26

#define STEP_PULSE_US 500 // ความกว้างพัลส์ (ไมโครวินาที)

void stepAll(bool dirFL, bool dirFR, bool dirRL, bool dirRR, int speed_pct);
void stopAll();

void setup() {
    Serial.begin(115200);

    pinMode(FL_STEP, OUTPUT); pinMode(FL_DIR, OUTPUT);
    pinMode(FR_STEP, OUTPUT); pinMode(FR_DIR, OUTPUT);
    pinMode(RL_STEP, OUTPUT); pinMode(RL_DIR, OUTPUT);
    pinMode(RR_STEP, OUTPUT); pinMode(RR_DIR, OUTPUT);

    stopAll();
    Serial.println("ESP32 TB6600 Controller Ready");
}

void loop() {
    if (Serial.available()) {
        String line = Serial.readStringUntil('\n');
        line.trim();
        if (line.length() == 0) return;

        if (line.startsWith("F:")) { // Forward
            int spd = line.substring(2).toInt();
            stepAll(HIGH, HIGH, HIGH, HIGH, spd);
        }
        else if (line.startsWith("B:")) { // Backward
            int spd = line.substring(2).toInt();
            stepAll(LOW, LOW, LOW, LOW, spd);
        }
        else if (line.startsWith("L:")) { // Left turn
            int spd = line.substring(2).toInt();
            stepAll(LOW, HIGH, LOW, HIGH, spd);
        }
        else if (line.startsWith("R:")) { // Right turn
            int spd = line.substring(2).toInt();
            stepAll(HIGH, LOW, HIGH, LOW, spd);
        }
        else if (line == "S") { // Stop
            stopAll();
            delay(10);
        }

        Serial.printf("Got: %s\n", line.c_str());
    }
}

void stepAll(bool dirFL, bool dirFR, bool dirRL, bool dirRR, int speed_pct) {
    // แปลง speed_pct (0-100) เป็น delay
    int delay_ms = map(constrain(speed_pct, 0, 100), 0, 100, 20, 1);

    digitalWrite(FL_DIR, dirFL);
    digitalWrite(FR_DIR, dirFR);
    digitalWrite(RL_DIR, dirRL);
    digitalWrite(RR_DIR, dirRR);

    // ส่งพัลส์พร้อมกัน
    digitalWrite(FL_STEP, HIGH);
    digitalWrite(FR_STEP, HIGH);
    digitalWrite(RL_STEP, HIGH);
    digitalWrite(RR_STEP, HIGH);
    delayMicroseconds(STEP_PULSE_US);
    digitalWrite(FL_STEP, LOW);
    digitalWrite(FR_STEP, LOW);
    digitalWrite(RL_STEP, LOW);
    digitalWrite(RR_STEP, LOW);

    delay(delay_ms);
}

void stopAll() {
    // ไม่ทำอะไร → มอเตอร์หยุด (ไม่มีพัลส์)
}
