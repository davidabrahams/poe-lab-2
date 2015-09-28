import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import json
import os
from numpy import sin, cos, radians
from matplotlib.mlab import griddata
from matplotlib.colors import LogNorm
# import seaborn as sns

toplevel_dir = os.path.join(os.path.dirname(__file__),
    os.path.pardir,
    os.path.pardir)

filename = os.path.join(toplevel_dir, "data", "data.txt")
v_points = 40
h_points = 40

h_deg_center = 90.0
v_deg_center = 90.0

h_deg_range = 45.0
v_deg_range = 45.0

camera_distance_from_center = 1.25  # inches

thresh_distance = 50  # inches
cut_off = 17

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
    """
    >>> get_angles(np.array([28]), h_degrees_min, h_degrees_max, h_points)
    array([ 99.])
    >>> get_angles(np.array([9]), v_degrees_min, v_degrees_max, v_points)
    array([ 77.625])

    """
    angles = anglemin + (indices.astype(float) / steps) * (anglemax - anglemin)
    return angles

def get_cartesian(h_pos_servos, v_pos_servos, distances):
    # get the angles from servo positions
    h_rads = radians(get_angles(h_pos_servos, h_degrees_min, h_degrees_max, h_points))
    v_rads = radians(get_angles(v_pos_servos, v_degrees_min, v_degrees_max, v_points))

    # adjust for camera offset
    distance_adj = distances - camera_distance_from_center

    x = distance_adj*sin(v_rads)*cos(h_rads)
    y = distance_adj* sin(v_rads)*sin(h_rads)
    z = distance_adj*cos(v_rads)

    return np.array([x, y, z]).T


def plot_points(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, alpha=0.07)
    ax.set_xlabel('X Position (inches)')
    ax.set_ylabel('Y Position (inches)')
    ax.set_zlabel('Z Position (inches)')
    plt.show()

def plot_heat(x, y, z, log=False):
    xi = np.linspace(-15, 15, 50)
    zi = np.linspace(-15, 15, 50)
    yi = griddata(x, z, y, xi, zi, interp='linear')

    if log:
        plt.pcolor(xi, zi, yi, norm=LogNorm(vmin=yi.min(), vmax=yi.max()))
    else:
        plt.pcolor(xi, zi, yi)
    cbar = plt.colorbar()

    ax = plt.gca()
    ax.set_xlabel('X Position (inches)')
    ax.set_ylabel('Z Position (inches)')
    cbar.set_label('Y Position (inches)')

    plt.show()

def plot_bool(x, y, z):
    xi = np.linspace(-15, 15, 50)
    zi = np.linspace(-15, 15, 50)
    yi = griddata(x, z, y, xi, zi, interp='linear')
    yi = yi <= cut_off

    plt.pcolor(xi, zi, yi)
    cbar = plt.colorbar()

    ax = plt.gca()
    ax.set_xlabel('X Position (inches)')
    ax.set_ylabel('Z Position (inches)')
    cbar.set_label('Y Position (inches)')

    plt.show()

def main():
    #Creates 3d plot from data points
    points = read_data(filename)
    distances = points[:,0]
    h_pos_servo = points[:,1]
    v_pos_servo = points[:,2]
    cartesian= get_cartesian(h_pos_servo, v_pos_servo, distances)
    cartesian = cartesian[cartesian[:, 1] <= thresh_distance]
    x, y, z = cartesian[:, 0], cartesian[:, 1], cartesian[:, 2]
    # plot_bool(x, y, z)
    plot_points(x, y, z)

if __name__ == '__main__':
    main()
