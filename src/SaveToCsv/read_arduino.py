import serial
import threading
import json
import math

# TODO: THIS IS SO WRONG.
def calibration(d):
    d = 3.95*math.exp(-.06*d)
    return d

def read_arduino():
    while running:
        line = ser.readline()
        d = float(line[:4])
        d = calibration(d)
        print "%f inches" % d
        distances.append(d)

def save_data():
    with open('data.txt', 'w') as outfile:
        json.dump(distances, outfile)


if __name__ == '__main__':

    running = True
    distances =[]
    ser = serial.Serial('/dev/ttyACM1', 9600)

    t = threading.Thread(target =read_arduino)
    s = raw_input('Press s to start! --> ')
    t.start()
    q = raw_input('Press q to quit! --> ')
    running = False
    save_data()



