import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import json
import os

toplevel_dir = os.path.join(os.path.dirname(__file__),
    os.path.pardir,
    os.path.pardir)
filename = os.path.join(toplevel_dir, "data.txt")
v_points =10
h_points =20
h_degrees_min = -45
h_degrees_max = 45
v_degrees_min = -22.5
v_degrees_max = 22.5


def read_data(fn):
    #takes in file name (ex: data.txt)
    #reads scanner data
    with open(fn) as file_obj:
        scanner_data = json.load(file_obj)
    data_points=np.array(scanner_data)

    return data_points


def get_angles(indices, anglemin, anglemax, steps):
    angle = anglemin + (indices.astype(float) / steps) * (anglemax - anglemin)
    return angle

def get_cartesian(data_points):
    pass


    def plot_points(x, y, z):
    pass


def main():
    #Creates 3d plot from data points
    points = read_data(filename)
    distances = points[:,0]
    h_pos_servo = points[:,1]
    v_pos_servo = points[:,2]
    h_angles = get_angles(h_pos_servo, h_degrees_min, h_degrees_max, h_points)
    v_angles = get_angles(v_pos_servo, v_degrees_min, v_degrees_max, v_points)
    print h_angles

if __name__ == '__main__':
    main()
