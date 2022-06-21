#include <Arduino_JSON.h>

#include <Wire.h>
#include <Adafruit_MPL115A2.h>
#include  <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>


Adafruit_MPL115A2 mpl115a2;
bool sFound = true;
int LDRPin = 2;
String cloudQuery = "http://18.224.110.169:727/sensorUpdate?key=eBk6RcZ8DC33aFR81kwe?";


int red = 14;
int green = 12;
int blue = 13;

int buzzer = 15;
void setup(void) 
{
  Wire.begin();


  pinMode(LDRPin, INPUT);
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(blue, OUTPUT);
  pinMode(buzzer, OUTPUT);
  
  Serial.begin(9600);
  Serial.println("NodeMCU is starting");
  WiFi.begin("Test_NMCU", "basculin");
  while (WiFi.status() != WL_CONNECTED) 
          {
            delay(500);
            Serial.print("Connecting to the internet.");
          }
  /*
  while (WiFi.status() != WL_CONNECTED) 
          {
            delay(500);
            Serial.print(".");
          }
         
  Serial.println("Connection successful!"); */
  Serial.println("Getting barometric pressure ...");
  mpl115a2.begin();
  if (! mpl115a2.begin()) {
    Serial.println("Sensor not found! Check wiring");
    sFound = false;
  }

  
}

void loop(void) 
{
  WiFiClient client;
  HTTPClient http;
  String cloudQuery = "http://18.224.119.169:727/sensorUpdate?key=eBk6RcZ8DC33aFR81kwe";
  
  int MQ7Value = analogRead(A0);
  if (sFound){
  float pressureKPA = 0, temperatureC = 0;    

  mpl115a2.getPT(&pressureKPA,&temperatureC);
  Serial.print("Pressure (kPa): "); Serial.print(pressureKPA, 4); Serial.print(" kPa  ");
  Serial.print("Temp (*C): "); Serial.print(temperatureC, 1); Serial.println(" *C both measured together");
  
  pressureKPA = mpl115a2.getPressure();  
  Serial.print("Pressure (kPa): "); Serial.print(pressureKPA, 4); Serial.println(" kPa");

  temperatureC = mpl115a2.getTemperature();  
  Serial.print("Temp (*C): "); Serial.print(temperatureC, 1); Serial.println(" *C");
  cloudQuery = cloudQuery + "&temp="+temperatureC+"&psure="+pressureKPA;
  }
  cloudQuery = (cloudQuery + "&ldr=" + digitalRead(LDRPin) + "&co=" + MQ7Value);
  http.begin(client, cloudQuery.c_str());

  int httpResponseCode = http.GET();
  
  if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        JSONVar payload = JSON.parse(http.getString());
        int redSet = payload[1];
        int blueSet = payload[2];
        int greenSet = payload[3];
        analogWrite(red, redSet);
        analogWrite(blue, blueSet);
        analogWrite(green, greenSet);
        
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      // Free resources
      http.end();
  
  delay(5000);

  
  
  

  
 
  /*
  Serial.println("Current CO Values: "); Serial.print(sensorValue);

  Serial.println("Current Light Values: "); 
  if (digitalRead(LDRPin)== HIGH){
    Serial.print("Light isn't too much");
    //HIGH: Işık yok
  }
  else{
    Serial.print("Light is too much, do operation");
    //LOW: Işık var
  }
  */
  
  
  
  
  
}
