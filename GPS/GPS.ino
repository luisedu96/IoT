#include <SoftwareSerial.h>
static const int RXPin = 2, TXPin = 0;
static const uint32_t GPSBaud = 9600;
// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);

String oracion = "";
void setup()
{
  Serial.begin(9600);
  ss.begin(GPSBaud);
  Serial.println("iniciando el programa");
}
void loop()
{
  while (ss.available() > 0)
  {
    int anInt = ss.read();
    char achar = anInt;
    oracion.concatenate()
    
    Serial.print(achar);
  }
  Serial.print("finnnnnnnnn");
}
