#include <ClosedCube_HDC1080.h>
#include <Wire.h>

ClosedCube_HDC1080 sensor;

void setup() {
sensor.begin(0x40);
Serial.begin(9600);
}

void loop() {
  double temperatura = sensor.readTemperature();
  double humedad = sensor.readHumidity();
  Serial.print("Temperatura = ");
  Serial.print(temperatura);
  Serial.print("°C humedad = ");
  Serial.print(humedad);
  Serial.println("°C");
  delay(3000);

}
