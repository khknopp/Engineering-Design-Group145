#include <ArduinoBLE.h>

BLEService randomService("180D");  // Create a BLE service using a custom UUID
BLEIntCharacteristic randomCharacteristic("2A37", BLERead);

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
      int randomNumber = random(0, 1024);
      randomCharacteristic.writeValue(9985071436);
      delay(1000);
    }

    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}