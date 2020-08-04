
#include <TinyGPS++.h> 
#include <SoftwareSerial.h>
#include <ClosedCube_HDC1080.h>
#include <Wire.h>

#define ESP82_GPS_RX 2
#define ESP82_GPS_TX 0

static float suma = 0;
static float promedio = 0;
static bool precision = false;
static bool decodificacion = false;
uint32_t t_sleep = 60;//segundos
static int estado = 1;

static String Trama = "";
double inicio = millis();

TinyGPSPlus GPSL70;
SoftwareSerial ssGPS(ESP82_GPS_RX, ESP82_GPS_TX);
ClosedCube_HDC1080 sensor;

void setup()
{
  Serial.begin(9600);
  ssGPS.begin(9600);
  sensor.begin(0x40);
  Serial.println();
  Serial.println("Iniciando...");
  residuos();
}

void loop()
{
  switch (estado)
  {
    case 1:
          decodificar_nmea();
          if(decodificacion) estado = 2;
          else estado=1;       
    break;
    case 2:
          confiabilidad_Datos();
          if(precision) estado=3;
          else estado=1;
    break;
    case 3:
          muestra_Datos();
          estado=4;
    break;
    case 4:
          Serial.print("Tiempo prendido: ");Serial.println(millis()-inicio);
          estado=1;
          dormir();
    break;
  }
}

void decodificar_nmea()
{
  while (ssGPS.available()>0)
  {
    if(GPSL70.encode(ssGPS.read())) decodificacion=true;
  }
}

void Posicion()
{
  static String posicion = "";
  static float la = 0;
  static float lo = 0;
  float LA = GPSL70.location.lat();
  float LO = GPSL70.location.lng();

  if(LA>0) la=LA;
  else la=-1*LA;

  if(LO>0) lo=LO;
  else lo=-1*LO;
  
  float lam = (la-int(la))*60;
  float las = (lam-int(lam))*60;
 
  Trama.concat(',');
  posicion.concat(String(int(la)));
  posicion.concat("°");
  posicion.concat(String(int(lam)));
  posicion.concat("'");
  posicion.concat(String(las,2));
  posicion.concat('"');
  if(LA>0) posicion.concat('N');
  else posicion.concat('S');

  float lom = (lo-int(lo))*60;
  float los = (lom-int(lom))*60;

  posicion.concat(' ');
  posicion.concat(String(int(lo)));
  posicion.concat("°");
  posicion.concat(String(int(lom)));
  posicion.concat("'");
  posicion.concat(String(los,2));
  posicion.concat('"');
  if(LO>0) posicion.concat('O');
  else posicion.concat('W');

  Trama.concat(posicion);
  Serial.print("Posición: ");
  Serial.println(posicion);
}

void Fecha()
{
  static String fecha = "";
  Trama.concat(',');
  int d = GPSL70.date.day();
  int m = GPSL70.date.month();
  int y = GPSL70.date.year();
  fecha.concat(d);
  fecha.concat('/');
  fecha.concat(m);
  fecha.concat('/');
  fecha.concat(y);
  Trama.concat(fecha);
  Serial.print("Fecha: ");Serial.println(fecha);
}

void Hora()
{
  static String hora = "";
  Trama.concat(',');
  int h = GPSL70.time.hour();
  int m = GPSL70.time.minute();
  int s = GPSL70.time.second();
  if(h<10)
  {
    hora.concat('0');
    hora.concat(String(h));
  }
  else hora.concat(String(h));
  hora.concat(':');
  if(m<10)
  {
    hora.concat('0');
    hora.concat(String(m));
  }
  else hora.concat(m);
  hora.concat(':');
  if(s<10)
  {
    hora.concat('0');
    hora.concat(s);
  }
  else hora.concat(s);
  hora.concat("GTM");
  hora.concat(String(int(GPSL70.location.lng()/15)));
  Trama.concat(hora);
  Serial.print("Hora: ");Serial.println(hora);
}

void Temperatura()
{ 
  static String temperatura = "";
  int i = 1;
  do
  {
    suma = suma + sensor.readTemperature();
    i++;
  }
  while(i<21);
  promedio=suma/20;
  temperatura.concat(String(promedio));
  temperatura.concat("°C");
  Trama.concat(temperatura);
  Serial.println("Temperatura = "+temperatura);
  promedio = 0;
  suma=0;
  i=1;
}

void Humedad()
{ 
  static String humedad = "";
  int i = 1;
  do
  {
    suma = suma + sensor.readHumidity();
    i++;
  }
  while(i<21);
  promedio=suma/20;
  Trama.concat(',');
  humedad.concat(String(promedio));
  humedad.concat('%');
  Trama.concat(humedad);
  Serial.println("Humedad = "+humedad);
  promedio=0;
  suma=0;
  i=1;
}

void confiabilidad_Datos()
{
  if(GPSL70.location.isValid() && GPSL70.date.isValid() && GPSL70.date.isValid() 
  && GPSL70.satellites.isValid())
  {
    precision = true;
  }
  else
  {
    precision = false;
  }
}

void muestra_Datos()
{
  Serial.println("Datos más precisos posibles");
  Temperatura();
  Humedad();
  Posicion();
  Fecha();
  Hora();
  Serial.print ("Trama creada: ");
  Serial.println(Trama);
}

void dormir()
{
  Serial.println("Modo sleep");
  Serial.println("-----------------------------------------------------");
  ESP.deepSleep(t_sleep*1000000, WAKE_RF_DISABLED);
}

void residuos()
{
  while(ssGPS.available()>0)
  {
    GPSL70.encode(ssGPS.read());
  }
}
