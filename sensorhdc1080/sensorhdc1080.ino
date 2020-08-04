#include <ClosedCube_HDC1080.h>
#include <Wire.h>

ClosedCube_HDC1080 sensor;
const double b=0;
const double m=1;
static int t=0;
static int h=0;

void setup() {
sensor.begin(0x40);
Serial.begin(9600);
}

void calibracion_temperatura(double T){
  double temperaturacalibrada=m*T+b;
  Serial.println("Temperatura calibrada = "+String(temperaturacalibrada)+" °C");
}

void calibracion_humedad(double H){
  double temperaturacalibrada=m*H+b;
  Serial.println("Humedad calibrada = "+String(temperaturacalibrada)+" %");
}

void T_promedio_muestras(double T){
  static double suma = 0;
  suma = suma + T;
  t++;
  if(t==20){
    delay(500);
    suma=suma/20;
    Serial.println("Temperatura promedio = "+String(suma)+" °C");
    suma=0;
    t=0;
  }
}

void H_promedio_muestras(double H){
  static double suma = 0;
  static double suma1 = 0;
  suma = suma + H;
  h++;
  if(h==20){
    delay(500);
    suma1=suma/20;
    Serial.println("Humedad promedio = "+String(suma1)+" %");//+String(suma));
    suma=0;
    h=0;
  }
}

void loop() {
  double temperatura = sensor.readTemperature();
  double humedad = sensor.readHumidity();
  Serial.println("Temperatura = "+String(temperatura)+" °C");
  Serial.println("Humedad = "+String(humedad)+" %");
  calibracion_temperatura(temperatura);
  calibracion_humedad(humedad);
  T_promedio_muestras(temperatura);
  H_promedio_muestras(humedad);
  delay(500);

}
