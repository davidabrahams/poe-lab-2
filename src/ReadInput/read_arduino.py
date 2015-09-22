import serial
import threading
import json
import math

running = True

class StopEvent:

    def __init__(self):
        self.is_set = False

    def set(self):
        self.is_set = True


def calibration(d):
    return d

def read_arduino(distances, ser, stop_event):
    while not stop_event.is_set:
        line = ser.readline()
        d = float(line[:4])
        d = calibration(d)
        print "%f inches" % d
        distances.append(d)

def save_data(distances, fn):
    with open(fn, 'w') as outfile:
        json.dump(distances, outfile)

def main():
    distances =[]
    ser = serial.Serial('/dev/ttyACM0', 9600)
    stop_event = StopEvent()

    t = threading.Thread(target=read_arduino, args=(distances, ser, stop_event))
    s = raw_input('Press s to start! --> ')
    t.start()
    q = raw_input('Press q to quit! --> ')
    stop_event.set()
    running = False
    save_data(distances, 'data.txt')


if __name__ == '__main__':
    main()



