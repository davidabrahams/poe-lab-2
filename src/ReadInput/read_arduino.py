import serial
import threading
import json
import math

running = True

referenceMv = 5000
interval = 250  # mV
distance_list = [150, 140, 130, 100, 60, 50, 40, 35, 30, 25, 20, 15]  # distance in cm for each 250 mV

class StopEvent:

    def __init__(self):
        self.is_set = False

    def set(self):
        self.is_set = True


def calibration(val):
    mV = int(val) * referenceMv / 1023
    index = mV/interval
    if index >= len(distance_list) - 1:
        centimeters = distance_list[-1]
    else:
        index = mV / interval
        frac = (mV % 250) / float(interval)
        centimeters = distance_list[index] - ((distance_list[index] - distance_list[index + 1]) * frac)

    inches = centimeters / 2.54
    return inches

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


