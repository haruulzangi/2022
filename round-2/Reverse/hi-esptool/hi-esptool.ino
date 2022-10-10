void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

const uint8_t data[] = {0b100,0b1,0b1011,0b0101,0b000,0b00,0b1,0b0,0b000,0b00,0b0100,0b100,0b000,0b101,0b1011,0b011};
const uint8_t len[] = {3, 1, 4, 4, 3, 2, 1, 1, 3, 2, 4, 3, 3, 3, 4, 3};
const int flag_len = 16;

const int unit_delay = 250;
void dot() {
  Serial.print(".");
  digitalWrite(LED_BUILTIN, HIGH);
  delay(unit_delay);
  digitalWrite(LED_BUILTIN, LOW);
  delay(unit_delay);
}

void dash() {
  Serial.print("-");
  digitalWrite(LED_BUILTIN, HIGH);
  delay(unit_delay * 3);
  digitalWrite(LED_BUILTIN, LOW);
  delay(unit_delay);
}

void write_flag() {
  for (int i = 0; i < flag_len; i++) {
    int mask = 1 << (len[i] - 1);
    while (mask) {
      if (data[i] & mask) {
        dot();
      } else {
        dash();
      }
      delay(unit_delay);
      mask >>= 1;
    }
  }
}

void loop() {
  write_flag();
  delay(unit_delay * 7);
}
