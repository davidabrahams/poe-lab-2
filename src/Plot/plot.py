import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import json
import os
from numpy import sin, cos, radians

toplevel_dir = os.path.join(os.path.dirname(__file__),
    os.path.pardir,
    os.path.pardir)

filename = os.path.join(toplevel_dir, "data", "data.txt")
v_points = 20
h_points = 20

h_deg_center = 90.0
v_deg_center = 90.0

h_deg_range = 45.0
v_deg_range = 45.0

# Due to how our servos and sensor are oriented, at a high index the sensor
# looks down and left
h_degrees_min = h_deg_center - h_deg_range / 2
h_degrees_max = h_deg_center + h_deg_range / 2
v_degrees_min = v_deg_center - v_deg_range / 2
v_degrees_max = v_deg_center + v_deg_range / 2


def read_data(fn):
    #takes in file name (ex: data.txt)
    #reads scanner data
    with open(fn, 'r') as file_obj:
        scanner_data = json.load(file_obj)
    data_points=np.array(scanner_data)

    return data_points


def get_angles(indices, anglemin, anglemax, steps):
    angle = anglemin + (indices.astype(float) / steps) * (anglemax - anglemin)
    return angle

def get_cartesian(h_angles, v_angles, distances):
    h_rads = radians(h_angles)
    v_rads = radians(v_angles)

    x = distances*sin(v_rads)*cos(h_rads)
    y = distances* sin(v_rads)*sin(h_rads)
    z = distances*cos(v_rads)

    return np.array([x, y, z]).T


def plot_points(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()



def main():
    #Creates 3d plot from data points
    points = read_data(filename)
    distances = points[:,0]
    h_pos_servo = points[:,1]
    v_pos_servo = points[:,2]
    h_angles = get_angles(h_pos_servo, h_degrees_min, h_degrees_max, h_points)
    # print h_angles
    v_angles = get_angles(v_pos_servo, v_degrees_min, v_degrees_max, v_points)
    print v_angles
    cartesian= get_cartesian(h_angles, v_angles, distances)
    x, y, z = cartesian[:, 0], cartesian[:, 1], cartesian[:, 2]
    plot_points(x, y, z)

if __name__ == '__main__':
    main()
