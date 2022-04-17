#include <Wire.h>
#include "MKRWAN.h"
#include <OneWire.h>
#include <DallasTemperature.h>
#include "arduino_secrets.h"
/******************************************************************************
  ParamÃ¨tres
*******************************************************************************/

int del = 2000;         //delay in milliseconds

//variables du serveur 

//Seuils
float T_treshold = 30;   //Max temp before ON
float H_treshold = 40;   //Min hum before ON
float H_treshold_stop = 100;
float T_treshold_stop = -10;
byte A = 0;

//variables
int Activate = A0;
int Temp = A1;
int Hum = A2;
int enable_T = A6;
int enable_H = A4;
int state = 0;
float humidity = 0;
float temperature = 0;

bool sensors = false;
bool internet = true;
bool se = false;

String stringSeparator;

/******************************************************************************
  Module LoRa Arduino MKR WAN 1300
*******************************************************************************/
LoRaModem modem;

void LORA_INIT() {
  
  if (!modem.begin(EU868)) {
    Serial.println("Echec du dÃ©marrage du module");
  }
  else
  {
    Serial.println(modem.begin(EU868));
    }

  // Affichage de la version du firmware de l'Arduino MKR WAN 1300
  //Serial.print("La version du firmware de l'Arduino MKR WAN 1300 est: ");
  //Serial.println(modem.version());
  
  // Affichage de l'EUI (End-device Unique Identifier)
  Serial.println("L'EUI (End-device Unique Identifier) est: ");
  Serial.println(modem.deviceEUI());

  int connected = modem.joinOTAA(SECRET_APP_EUI, SECRET_APP_KEY);
  if (!connected) {
    Serial.println("Conection problem");

  }
  else {
    state = 1;
    //digitalWrite(Activate, LOW);
    Serial.println("Connected");
  }
}

//--------------------------------------------------------------------------//
void setup()
{
  Bridge.begin();
  Serial.begin(115200);   // ouvre le port sÃ©rie USB Ã  115200 baud
  delay(500);
  
  // Setup pins
  pinMode(Activate, OUTPUT);
  pinMode(Hum, INPUT);
  pinMode(Temp, INPUT);
  pinMode(enable_T, OUTPUT);
  pinMode(enable_H, OUTPUT);

}
//--------------------------------------------------------------------------//

void getHum()
{
  digitalWrite(enable_H, HIGH) ;  //Enable sensor
  delay(100);
  
  float sensorValue = 0;

  sensorValue = sensorValue + analogRead(Hum);
  sensorValue = map(sensorValue, 0, 3.3, 0, 100);
  digitalWrite(enable_H, LOW);

  humidity = sensorValue / 100;

}

//--------------------------------------------------------------------------//
void getT()
{
  OneWire oneWire(Temp);
  // Pass our oneWire reference to Dallas Temperature.
  DallasTemperature sensors(&oneWire);
  sensors.begin();

  digitalWrite(enable_T, HIGH) ;//Enable sensor
  delay(100);
  
  sensors.requestTemperatures(); // Send the command to get temperatures
  float tempC = sensors.getTempCByIndex(0);

  // Check if reading was successful
  if (tempC != DEVICE_DISCONNECTED_C)
  {
    temperature = tempC;
  }
  else
  {
    Serial.println("Erreur : Impossible de lire les donnÃ©es de tempÃ©rature");
  }
  digitalWrite(enable_T, LOW);
}

//--------------------------------------------------------------------------//
void sendInfo()
{
  // Mise en forme du message
  stringSeparator = " ";

  uint32_t T = temperature * 100;
  uint32_t H = humidity * 100;

  byte payload[5];
  payload[0] = highByte(H);
  payload[1] = lowByte(H);
  payload[2] = highByte(T);
  payload[3] = lowByte(T);
  payload[4] = A;

  // Envoi du message vers le rÃ©seau LoRa
  modem.beginPacket();

  modem.write(payload, 5);
  int err = modem.endPacket(true);
  
  // VÃ©rification
  if (err > 0) {
    Serial.println("Message bien envoyÃ©");
    //Serial.println();
  } else {
    Serial.println("Erreur lors de l'envoi du message :-(");
    //Serial.println("(Pensez Ã  envoyer un nombre limitÃ© de messages par minute en fonction de la force du signal");
    //Serial.println("la frÃ©quence d'envoi peut varier d'un message toutes les quelques secondes Ã  un message par minute.)");
    Serial.println();
    state == 0;
  }
}

//RX msg

void Rx_msg() {

  if (modem.available())
  {
    char rcv[64];
    int i = 0;
    while (modem.available()) {
      rcv[i++] = (char)modem.read();
    }

    for (unsigned int j = 0; j < i; j++) {
      //Serial.print(rcv[j] >> 4);
      //Serial.print(rcv[j] & 0xF);
      Serial.print(" ");
    }
    //Serial.println(rcv[0]);
    if (rcv[0]  == 'A') {
      internet = true;
      A = 1;
    }
    if (rcv[0] == 'B') {
      internet = false;
      A = 0;
    }

  }
}

//--------------------------------------------------------------------------//
void loop()
{
  //connect to server
  Serial.println("connection to server: ");
  //connectToServer();
  // Programme principal
  if (state == 0) //INITIALIZING
  {
     
    LORA_INIT();
  }
  
  sensors = (temperature > T_treshold or humidity < H_treshold) and humidity < H_treshold_stop; //from python

  
  if (state == 1) //Sensing & Send
  {
    getHum();
    getT();

    if (internet)
    {
      if (sensors) {
        digitalWrite(Activate, HIGH);
        A = 1;

      }
      else
      {
        digitalWrite(Activate, LOW);
        A = 0;
      }
    }
    else {
      digitalWrite(Activate, LOW);
      A = 0;
    }
  }
  
  se = not se;
  if (se) {
    sendInfo();
    Rx_msg();
  }


  // Ecrit les donnÃ©es sur le port sÃ©rie
  Serial.print("temperature:");
  Serial.print(temperature);
  Serial.print(" CÂ° ");
  Serial.print('x');
  Serial.print("Humidity:");
  Serial.print(humidity);
  Serial.println( "%");

  // Pause de X millisecondes
  delay(del);
}
