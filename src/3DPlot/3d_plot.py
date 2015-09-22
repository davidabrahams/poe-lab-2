import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import json
import os

toplevel_dir = os.path.join(os.path.dirname(__file__),
    os.path.pardir,
    os.path.pardir)
filename = os.path.join(toplevel_dir, "data.txt")

def read_data(fn):
	#takes in file name (ex: data.txt)
	#reads scanner data
	with open(fn) as file_obj:
		scanner_data = json.load(file_obj) 
	

	data_points=np.array(scanner_data)

	return data_points

def main():
	#Creates 3d plot from data points
	print read_data(filename)


if __name__ == '__main__':
    main()