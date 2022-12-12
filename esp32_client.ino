// SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
//
// SPDX-License-Identifier: MIT

/*
  Web client

 This sketch connects to a website (wifitest.adafruit.com/testwifi/index.html)
 using the WiFi module.

 This example is written for a network using WPA encryption. For
 WEP or WPA, change the Wifi.begin() call accordingly.

 This example is written for a network using WPA encryption. For
 WEP or WPA, change the Wifi.begin() call accordingly.

 created 13 July 2010
 by dlf (Metodo2 srl)
 modified 31 May 2012
 by Tom Igoe
 */

#include <WiFi.h>
#include <WiFiUdp.h>

// Enter your WiFi SSID and password
char ssid[] = "Zi-Net";   // your network SSID (name)
char pass[] = "password"; // your network password (use for WPA, or use as key for WEP)

unsigned int udpPort = 2399;
const char *udpAddress = "192.168.4.1";

int status = WL_IDLE_STATUS;

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
WiFiClient client;
WiFiUDP udp;
int incomingByte = 0; // for incoming serial data

void setup()
{
    // Initialize serial and wait for port to open:
    Serial.begin(115200);
    while (!Serial)
    {
        ; // wait for serial port to connect. Needed for native USB port only
    }
    //    pinMode(pushSwitch.pin, INPUT_PULLUP);

    pinMode(GPIO_NUM_32, INPUT);
    pinMode(GPIO_NUM_33, OUTPUT);
    // attempt to connect to Wifi network:
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);

    WiFi.begin(ssid, pass);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("Connected to WiFi");
    printWifiStatus();
    digitalWrite(GPIO_NUM_33, HIGH);
    esp_sleep_enable_ext0_wakeup(GPIO_NUM_32, 0);
}

void loop()
{
    if (digitalRead(GPIO_NUM_32) == HIGH)
    {
        digitalWrite(GPIO_NUM_33, LOW);
        Serial.println("sleeping");
        esp_deep_sleep_start();
    }

    if (Serial.available() > 0)
    {
        // read the incoming byte:
        incomingByte = Serial.read();

        uint8_t buffer[1] = {char(incomingByte)};
        // This initializes udp and transfer buffer
        udp.beginPacket(udpAddress, udpPort);
        udp.write(buffer, 1);
        udp.endPacket();
    }
}

void printWifiStatus()
{
    // print the SSID of the network you're attached to:
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());

    // print your board's IP address:
    IPAddress ip = WiFi.localIP();
    Serial.print("IP Address: ");
    Serial.println(ip);

    // print the received signal strength:
    long rssi = WiFi.RSSI();
    Serial.print("signal strength (RSSI):");
    Serial.print(rssi);
    Serial.println(" dBm");
}