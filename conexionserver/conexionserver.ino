#include <ESP8266WiFi.h>
const char* ssid = "TIGO-B6F1";
const char* password = "2NJ557301874";
//const char* ssid = "UPBWiFi";
//const char* password = "";
//poner la direccion IP del servidor
const char* server = "35.174.0.161";
double latitud= 6.2455678;
double longitud= -75.4678888;
double temperatura = 23;
int id = 1001;
WiFiClient client;

void setup()
{

 Serial.begin(115200);

 delay(10);

 pinMode(A0, INPUT);

 WiFi.begin(ssid, password);

 Serial.println();

 Serial.println();

 Serial.print("Connecting to ");

 Serial.println(ssid);

 WiFi.begin(ssid, password);

 while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.print(".");

 }

 Serial.println("");

 Serial.println("WiFi connected");

}

void loop()
{
  delay(5000);
  sendthingspeak();
  temperatura = random(10,35);
}

void sendthingspeak()
{
 String PostData = "";
 Serial.println("datos para enviar");
 PostData = String("id="+String(id)+"; temperatura="+String(temperatura,7)+"; longitud="+String(longitud,7)+"; latitud="+String(latitud,7));
 Serial.println(PostData);
 if ( client.connect(server,80))
 {
  Serial.println("conectado");
  client.print("POST /datos HTTP/1.1\n");
  // poner la direccion IP del servidor 
  client.print("Host: 35.174.0.161 \n");
  client.println("User-Agent: Arduino/1.0");
  client.println("Connection: close");
  client.println("Content-Type: application/x-www-form-urlencoded;");
  client.print("Content-Length: ");
  client.println(PostData.length());
  client.println();
  client.println(PostData);
 }
 else
 {
  Serial.println("error de conexion");
 }
}
