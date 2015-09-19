import serial
import threading
import json
import math

distances =[]

running = True

t = threading.Thread(target = read_arduino)
s = raw_input('Press s to start')
t.start()
q = raw_input('Press q to quit')
running = False
ser = serial.Serial('/dev/ttyACM0', 9600)

def calibration(d):
	d = 3.95*math.exp(-.06*d)
def read_arduino():
	while running:
    	line = ser.readline()
    	d = float(line)
    	d = 
    	distances.append(float(line))

def save_data():
	with open('data.txt', 'w') as outfile:
		json.dump(distances, outfile)



