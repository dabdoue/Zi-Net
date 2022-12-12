import XBee
import time
import serial
import threading
import RPi.GPIO as GPIO


def sleep_esp32():
    GPIO.output(23, GPIO.HIGH)  # sends high signal that puts esp32 to sleep
    print("esp32 sleeping...")


def wakeup_esp32(cur_esp32):
    print("waking up esp32: " + str(time.time()))
    GPIO.output(23, GPIO.LOW)  # sends low signal that triggers esp32 wakeup

    cur_esp32.waking_up = True
    time_in_10 = time.time() + 10
    # while not received signal from esp32 indicating it is awake, stay in while loop
    while not GPIO.input(24):
        continue

    cur_esp32.on = True
    cur_esp32.waking_up = False
    print("esp32 awake now: " + str(time.time()))
    cur_esp32.changed_recently = True


def send_zigbee_message(letter, xbee_sender):
    # print("Sent Message: ")
    xbee_sender.SendStr(letter)
    time.sleep(0.25)
    # xbee_sender.Receive()
    print("sending the following message via zigbee: " +
          letter + " time: " + str(time.time()))


def send_esp32_message(letter, esp32):
    esp32.write(bytes(letter, 'utf-8'))
    print("sending the following message via esp32: " +
          letter + " time: " + str(time.time()))


class Esp32(object):
    def __init__(self, power_status, changed_recently, waking_up):
        self.on = power_status
        self.changed_recently = changed_recently
        self.waking_up = waking_up


def read_zigbee_message(xbee_receiver):
    while True:
        # print("Received Message: ")
        xbee_receiver.Receive()
        time.sleep(0.25)


xbee_sender = XBee.XBee("/dev/ttyACM0")  # Your serial port name here
xbee_receiver = XBee.XBee("/dev/ttyACM1")  # Your serial port name here

esp32 = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)

# message = "This is a demonstration of the incredible capabailities of the Zi-Net system, created by Daniel Abdoue and Anit Kapoor."
# message = "\nHarry Potter is a series of seven fantasy novels\n"
message = "\nHarry Potter is a series of seven fantasy novels\n"
num_loops = 0
time_to_sleep = 0
previous_message_time = 0
current_message_time = 0
slow_time = 0.5
fast_time = 0.1

data_rate_threshold = 0.15


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

cur_esp32 = Esp32(False, False, False)
esp32_wakeup = threading.Thread(
    target=wakeup_esp32, args=(cur_esp32,))


# f.close()
zigbee_receive_thread = threading.Thread(
    target=read_zigbee_message, args=(xbee_receiver,))
zigbee_receive_thread.start()

# A simple string message
while True:

    try:
        if num_loops % 2 == 0:
            time_to_sleep = slow_time
        else:
            time_to_sleep = fast_time

        for letter in message:
            if cur_esp32.on and cur_esp32.changed_recently:
                # print("esp32 status changed recently")
                esp32_wakeup.join()  # join previous thread once esp32 wakes up
                # creates new instance of thread to be started when waking up esp again
                esp32_wakeup = threading.Thread(
                    target=wakeup_esp32, args=(cur_esp32,))
                time_to_sleep = fast_time
                cur_esp32.changed_recently = False
            elif cur_esp32.on and time.time() - previous_message_time > data_rate_threshold:
                sleep_esp32()
                cur_esp32.on = False
            elif not cur_esp32.waking_up and not cur_esp32.on and time.time() - previous_message_time < data_rate_threshold:
                # print("starting esp32 wake up")
                esp32_wakeup.start()

            if cur_esp32.on and not cur_esp32.changed_recently:
                send_esp32_message(letter, esp32)

            else:
                send_zigbee_message(letter, xbee_sender)

            previous_message_time = time.time()
            if cur_esp32.waking_up:
                time.sleep(slow_time)
            else:
                time.sleep(time_to_sleep)
        num_loops += 1
        time.sleep(1)
        print()
    except KeyboardInterrupt:
        zigbee_receive_thread.join()
        esp32_wakeup.join()
        break
