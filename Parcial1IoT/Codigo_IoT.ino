#include <TinyGPS++.h> 
#include <SoftwareSerial.h>
#include <ClosedCube_HDC1080.h>
#include <Wire.h>

#define ESP82_GPS_RX 2
#define ESP82_GPS_TX 0

double inicio = millis();
static float suma = 0, promedio = 0;
double t_sleep = 60;//segundos
static int estado = 1;
bool precision = false, decodificacion = false;

static String temperatura = "", humedad = "", posicion = "", fecha = "", hora = "", Trama = "";

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
  residuos();//lee las tramas nmea acumulados en el puerto serial
}

void loop()
{
  Trama = ""; 
  switch (estado)
  {
    case 1:
          decodificar_nmea();//leer la trama nmea a travez de la biblioteca tinyGPSplus
          if(decodificacion) estado = 2;//decodificacion es de tipo booleano, si se hizo el proceso de leer la trama nmea éste será verdadero y pasará al estado siguiente. 
          else estado=1;//si decodificacion es falso se devolverá a1 estado 1.
          decodificacion = false;
          residuos();       
    break;
    case 2:
          confiabilidad_Datos();//evalúa la precision de los datos leidos del gps. 
          if(precision)//precision es de tipo booleano, si la evalucion es corecta precision es verdadero pasa al estado 3  
          {
            estado=3;
            Serial.println("Datos más precisos posibles");
          }
          else estado=1;// si la precision es falso se devuleve al estdo 1.
          precision = false;
          residuos();
    break;
    case 3:
          Temperatura();//capta informacion de temperatura del sensor y las convierte en datos.
          estado=4;
          residuos();
    break;
    case 4:
          Humedad();//capta informacion de humedad del sensor y la convierte en dato
          estado=5;
          residuos();
    break;
    case 5:
          Posicion();//toma los datos leidos por el tinygpsplus y seleciona latitud y longitud
          estado=6;
          residuos();
    break;
    case 6:
          Fecha();//toma los datos leidos por el tinygpsplus y seleciona la hora
          estado=7;
          residuos();
    break;
    case 7:
          Hora();//toma los datos leidos por el tinygpsplus y selecciona la fecha
          estado=8;
          residuos();
    break;
    case 8:
          Armar_Trama();//toma todos los datos obtenidos (temperatura, humedad, posicion, fecha, hora) y arma la trama
          residuos();
    case 9:
          double tiempo_encendido = millis()-inicio;
          Serial.print("Tiempo ecendido: ");Serial.println(tiempo_encendido);
          estado=1;
          residuos();
          dormir(tiempo_encendido);//entra en el modo deepsleep para ahorrar energía.
    break;
  }
}

void decodificar_nmea()//codifica la trama nmea con la libreri tinygpsplus
{
  while (ssGPS.available()>0)
  {
    if(GPSL70.encode(ssGPS.read())) decodificacion=true;
  }
}

void Posicion()//tomar latitud y longitud la lectura que hizo tinygpsplus y convierte en grados minutos y segundos
{
  posicion = "";
  float la = 0 , lo = 0;
  float LA = GPSL70.location.lat(), LO = GPSL70.location.lng();

  if(LA>0) la=LA;
  else la=-1*LA;

  if(LO>0) lo=LO;
  else lo=-1*LO;
  
  float lam = (la-int(la))*60, las = (lam-int(lam))*60;
 
  posicion.concat(String(int(la)));posicion.concat("°");posicion.concat(String(int(lam)));posicion.concat("'");posicion.concat(String(las,2));posicion.concat('"');
  if(LA>0) posicion.concat('N');
  else posicion.concat('S');

  float lom = (lo-int(lo))*60, los = (lom-int(lom))*60;

  posicion.concat(',');posicion.concat(String(int(lo)));posicion.concat("°");posicion.concat(String(int(lom)));posicion.concat("'");posicion.concat(String(los,2));posicion.concat('"');
  if(LO>0) posicion.concat('O');
  else posicion.concat('W');

  Serial.print("Posición: ");
  Serial.println(posicion);
}

void Fecha()
{
  fecha="";
  int d = GPSL70.date.day(), m = GPSL70.date.month(), y = GPSL70.date.year();
  fecha.concat(d);fecha.concat('/');fecha.concat(m);fecha.concat('/');fecha.concat(y);
  Serial.print("Fecha: ");Serial.println(fecha);
}

void Hora()
{
  hora="";
  int h = GPSL70.time.hour(), m = GPSL70.time.minute(), s = GPSL70.time.second();
  if(h<10)
  {
    hora.concat('0');hora.concat(String(h));
  }
  else hora.concat(String(h));
  hora.concat(':');
  if(m<10)
  {
    hora.concat('0');hora.concat(String(m));
  }
  else hora.concat(m);
  hora.concat(':');
  if(s<10)
  {
    hora.concat('0');hora.concat(s);
  }
  else hora.concat(s);
  hora.concat("GTM"); hora.concat(String(int(GPSL70.location.lng()/15)));Serial.print("Hora: ");Serial.println(hora);
}

void Temperatura()
{ 
  temperatura = "";
  int i = 1;
  do
  {
    suma = suma + sensor.readTemperature();
    i++;
  }
  while(i<21);
  promedio=suma/20;
  temperatura.concat(String(promedio)), temperatura.concat("°C");Serial.println("Temperatura = "+temperatura);
  promedio = 0;
  suma=0;
  i=1;
}

void Humedad()
{ 
  humedad="";
  int i = 1;
  do
  {
    suma = suma + sensor.readHumidity();
    i++;
  }
  while(i<21);
  promedio=suma/20;
  humedad.concat(String(promedio));humedad.concat('%');
  Serial.println("Humedad = "+humedad);
  promedio=0;
  suma=0;
  i=1;
}

void confiabilidad_Datos()//analiza la preciion de los datos del gps para tener una mayor precision. 
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

void Armar_Trama()
{
  Serial.print ("Trama creada: ");
  Trama.concat(temperatura);Trama.concat(';');Trama.concat(humedad);Trama.concat(';');Trama.concat(posicion);Trama.concat(';');Trama.concat(fecha);Trama.concat(';');Trama.concat(hora); 
  Serial.println(Trama);
}

void dormir(double t)
{
  Serial.println("Modo sleep");
  Serial.println("-----------------------------------------------------");
  ESP.deepSleep(t_sleep*1000000, WAKE_RF_DISABLED);
  //delay(t_sleep*1000-t);
}

void residuos()
{
  while(ssGPS.available()>0)
  {
    GPSL70.encode(ssGPS.read());
  }
}
