#include <Servo.h>

Servo bahuY; // Shoulder up-down
Servo bahuX; // Shoulder rotation
Servo sikut; // Elbow
Servo servo4; // Additional servo (can be used for wrist pitch)
Servo lengan; // Wrist up-down
Servo griper; // Gripper

String validCommands[] = {
  "hijau1,merah1", "hijau1,merah1", "biru1,hijau1,merah1", 
  "biru1,merah1,hijau1", "merah1,hijau1", "merah1,hijau1"
};

void setup() {
  Serial.begin(9600);

  bahuY.attach(5);  // kuning bahu naik turun
  bahuX.attach(6);  // hijau bahu putar
  sikut.attach(7);  // biru sikut
  servo4.attach(10);  // servo 4
  lengan.attach(9);  // lengan naik turun
  griper.attach(8); // griper

  delay(30);
  bahuY.write(100);
  bahuX.write(125);
  sikut.write(100);
  servo4.write(90);
  lengan.write(40);
  griper.write(160);

  Serial.println("Masukkan perintah warna seperti 'merah1'.");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.equalsIgnoreCase("hijau1")) {
      pickhijau();
      delay(1000);
      placehijau();
      delay(1000);
      reset();
    } else if (input.equalsIgnoreCase("merah1")) {
      pickmerah();
      delay(1000);
      placemerah();
      delay(1000);
      reset();
    } else {
      Serial.println("Perintah tidak dikenali. Coba 'hijau1', 'biru1', 'merah1' atau kombinasi yang valid.");
    }
  }
}

bool isValidCombo(String input) {
  for (int i = 0; i < sizeof(validCommands) / sizeof(validCommands[0]); i++) {
    if (input.equalsIgnoreCase(validCommands[i])) {
      return true;
    }
  }
  return false;
}

void slowMove(Servo &servo, int targetPos, int stepDelay) {
  int currentPos = servo.read();
  if (currentPos < targetPos) {
    for (int pos = currentPos; pos <= targetPos; pos++) {
      servo.write(pos);
      delay(stepDelay);
    }
  } else {
    for (int pos = currentPos; pos >= targetPos; pos--) {
      servo.write(pos);
      delay(stepDelay);
    }
  }
}

void pickmerah() {
  Serial.println("Mengambil objek merah...");
  slowMove(bahuX, 125, 15);
  slowMove(bahuY, 55, 15);
  slowMove(sikut, 95, 15);
  slowMove(lengan, 50, 15);
  delay(2000);
  slowMove(griper, 90, 15);
  delay(500);
  Serial.println("Objek merah diambil.");
}

void placemerah() {
  Serial.println("Menempatkan objek merah...");
  slowMove(bahuY, 100, 15);
  slowMove(bahuX, 50, 15);
  slowMove(sikut, 100, 15);
  slowMove(servo4, 90, 15);
  slowMove(lengan, 60, 15);
  slowMove(bahuY, 60, 15);
  delay(2000);
  slowMove(griper, 160, 15);
  delay(500);
  Serial.println("Objek merah ditempatkan.");
}

void pickhijau() {
  Serial.println("Mengambil objek merah...");
  slowMove(bahuX, 125, 15);
  slowMove(bahuY, 55, 15);
  slowMove(sikut, 95, 15);
  slowMove(lengan, 50, 15);
  delay(2000);
  slowMove(griper, 90, 15);
  delay(500);
  Serial.println("Objek merah diambil.");
}

void placehijau() {
  Serial.println("Menempatkan objek hijau...");
  slowMove(bahuY, 100, 15);
  slowMove(bahuX, 75, 15);
  slowMove(sikut, 100, 15);
  slowMove(servo4, 90, 15);
  slowMove(lengan, 60, 15);
  slowMove(bahuY, 60, 15);
  delay(2000);
  slowMove(griper, 160, 15);
  delay(500);
  Serial.println("Objek hijau ditempatkan.");
}

void reset() {
  slowMove(bahuY, 100, 15);
  slowMove(bahuX, 125, 15);
  slowMove(sikut, 100, 15);
  slowMove(servo4, 90, 15);
  slowMove(lengan, 40, 15);
  slowMove(griper, 160, 15);
}
