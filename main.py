import XBee
from time import sleep

if __name__ == "__main__":
    xbee_sender = XBee.XBee("/dev/ttyACM0")  # Your serial port name here
    xbee_receiver = XBee.XBee("/dev/ttyUSB0")
    # A simple string message
    while True:
        try:
            message = input("Send: ")
            sent = xbee_sender.SendStr(message)
            sleep(0.25)
            xbee_sender.Receive()
            # if Msg:
            #     content = Msg[7:-1].decode('ascii')
            #     print("Msg: " + content)
            print("Received Message: ")
            xbee_receiver.Receive()
            sleep(0.25)
        except KeyboardInterrupt:
            break

    # A message that requires escaping
    # xbee.Send(bytearray.fromhex("7e 7d 11 13 5b 01 01 01 01 01 01 01"))
    # sleep(0.25)
    # Msg = xbee.Receive()
    # if Msg:
    #     content = Msg[7:-1]
    #     print("Msg: " + xbee.format(content))
