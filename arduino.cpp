#include <ArduinoBLE.h>

BLEService randomService("180D");  // Create a BLE service using a custom UUID
BLEIntCharacteristic randomCharacteristic("2A37", BLERead);

const int F1_PIN = 3;
const int F2_PIN = 4;
const int F3_PIN = 5;
const int F4_PIN = 6;
const int P_PIN = 7;

int value;

void setup() {
  // Start serial communication for debugging
  Serial.begin(9600);
  while (!Serial);

  // Start BLE module
  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  // Add service and characteristic
  BLE.setLocalName("RP2040");
  BLE.setAdvertisedService(randomService);
  randomService.addCharacteristic(randomCharacteristic);
  BLE.addService(randomService);
  
  // Start advertising
  BLE.advertise();
  Serial.println("Bluetooth device active, waiting for connections...");
}

void loop() {
  // Wait for a BLE central device connection
  BLEDevice central = BLE.central();
  
  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());
    
    while (central.connected()) {
      // int randomNumber = random(0, 1024);
      value = map(analogRead(F1_PIN), 0, 1023, 0, 99);
      value *= 100;
      value = map(analogRead(F2_PIN), 0, 1023, 0, 99);
      value *= 100;
      value = map(analogRead(F3_PIN), 0, 1023, 0, 99);
      value *= 100;
      value = map(analogRead(F4_PIN), 0, 1023, 0, 99);
      value *= 100;
      value = map(analogRead(P_PIN), 0, 1023, 0, 99);
      randomCharacteristic.writeValue(value);
      delay(1000);
    }

    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}