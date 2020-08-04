#include <TinyGPS++.h> 
#include <SoftwareSerial.h>

#define ARDUINO_GPS_RX 0 
#define ARDUINO_GPS_TX 2 
TinyGPSPlus tinyGPS;
SoftwareSerial ssGPS(ARDUINO_GPS_TX, ARDUINO_GPS_RX);

void setup()
{
  Serial.begin(9600);
  ssGPS.begin(9600);
}

void loop()
{
  printGPSInfo();
  smartDelay(5000); 
}

void printGPSInfo()
{
  double grados = tinyGPS.location.lng();
  Serial.print("Lat: "); Serial.println(tinyGPS.location.lat(), 6);
  Serial.print("Long: "); Serial.println(grados, 6);
  Serial.print("Alt: "); Serial.println(tinyGPS.altitude.feet());
  Serial.print("Course: "); Serial.println(tinyGPS.course.deg());
  Serial.print("Speed: "); Serial.println(tinyGPS.speed.mph());
  Serial.print("Date: "); printDate();
  Serial.print("Time: "); printTime(grados);
  Serial.print("Sats: "); Serial.print(tinyGPS.satellites.value());Serial.print("-");Serial.println(bool(tinyGPS.satellites.isValid()));

  Serial.println();
}

static void smartDelay(unsigned long ms)
{
  unsigned long band = millis();
  do
  {
    while (ssGPS.available())
      tinyGPS.encode(ssGPS.read());
  } while (millis() - band < ms);
}

void printDate()
{
  Serial.print(tinyGPS.date.day());
  Serial.print("/");
  Serial.print(tinyGPS.date.month());
  Serial.print("/");
  Serial.println(tinyGPS.date.year());
}

void printTime(double grados)
{
  int hora=int(grados/15.0);
  double minutos=(grados-15*hora)*60;
  Serial.print((tinyGPS.time.hour()+hora));
  Serial.print(":");
  if (tinyGPS.time.minute() < 10) Serial.print('0');
  Serial.print(tinyGPS.time.minute());
  Serial.print(":");
  if (tinyGPS.time.second() < 10) Serial.print('0');
  Serial.println(tinyGPS.time.second());
}
