# Zi-Net

This project combines 802.15.4 and 802.11 to create a protocol that allows for power savings on sensor networks that occasionally require high data transmission rates.

## Hardware:
1. Raspberry Pi
2. Arduino Uno x2
3. XBee S2C x2
4. ESP32

![Hardware](hardware.jpg?raw=true "Hardware")

### This is essentially a system where the Raspberry Pi communicates with itself. 

One way it communicates is via 802.15.4, where an Arduino, wired to the XBee, connects to the Pi over USB. The Pi writes to the arduino which then writes a Zigbee dataframe to the XBee device.
Then, another XBee, wired to another arduino, which is connected to the Pi via USB, receives the data frame from the XBee, decodes it, and writes the data it receives to a file.

The other way that the Pi can talk to itself is via 802.11. The Pi is acting as a router creating it's own network, and the ESP32 connects to that network when booted. The Pi also runs a UDP netcat server, which the ESP32 sends UDP packets to, and what the netcat server receives is then written to a file.

## Protocol
The way our protocol works is that there is a threshold that determines whether to send data via 802.15.4 or 802.11 based on data transmission rates. This threshold is somewhat arbitrary, but is based around the max data rate of the XBee, plus some arbitrary time for system overhead. We measure the data transmission rate by checking the time between each packet being sent.

In the demo, there is a set data rate for a string to be transmitted one character at a time, representing packets. 

When the data transmission rate is below the threshold, the ESP32 is put to sleep, and the Pi writes to the arduino to send each character over 802.15.4, which then gets received by the other XBee, and that data is written to a file.

However, if the data transmission rate goes above the threshold, then the Pi wakes up the ESP32 by sending a high signal over GPIO that wakes up the ESP32, which then connects to the Pi's network. Once connected, the ESP32 send a signal back to the Pi over GPIO to say that it has woken up. This wake up process takes about 5 seconds on average, so while the Pi has not yet received the signal that the ESP32 is awake, it continues sending the data over 802.15.4. Likewise, once the data rate goes below the threshold, the ESP32 is put back to sleep and data transmission resumes over 802.15.4.

Here is an image displaying the data flow:
![data_flow](data_flow.png?raw=true "data_flow")

## Demo
Below is a video demoing this protocol. Here we are sending a string one character at a time, and we continuously send this string. Every other time the string is sent, the data rate is set to something faster than the XBee can handle, so that it switches to the ESP32, and then the next transmission will be at a slower data rate to show the XBees communicating.
In the window on the left side, you'll see the data being received from the XBee, and on the right, it will be data received from the ESP32.
You can also see in the terminal some status messages and what data is meant to be transmitted through which device.






https://user-images.githubusercontent.com/49587024/207107281-9d99256c-ecce-495b-9804-bd0050c70171.mp4



