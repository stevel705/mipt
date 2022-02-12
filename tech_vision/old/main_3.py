from warnings import catch_warnings
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon, LineString
from shapely.geometry.polygon import LinearRing

from skimage import transform
from scipy import spatial
from skimage.io import imshow, imread
from math import fabs, pi, atan2
from scipy.interpolate import make_interp_spline
from inters import intersection, line
from tqdm import tqdm
import math

import matplotlib.pyplot as plt
from skimage import transform


def get_line_by_points(a, b):
    L1 = line(a, b)
    
    x_t = np.linspace(-5, 5, 500)

    # if a[0] < b[0]:
    #     x_t = np.linspace(-5, 5, 500)
    # else:
    #     x_t = np.linspace(5, -5, 500)

    y_t = (L1[2] - (L1[0] * x_t)) / L1[1]

    # poly_line = [[x, y] for x, y in zip(x_t, y_t)]
    return x_t, y_t

def intersections(a, line):
    ea = LinearRing(a)
    mp = ea.intersection(line)
    if mp.is_empty:
        print('Geometries do not intersect')
        return [], []
    elif mp.geom_type == 'Point':
        return [mp.x], [mp.y]
    elif mp.geom_type == 'MultiPoint':
        return [p.x for p in mp], [p.y for p in mp]
    else:
        raise ValueError('something unexpected: ' + mp.geom_type)
          
def line_intersec(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    point_x = ((x2 - x1) * (y3 * x4 - y4 * x3) - (x4 - x3) * (y1 * x2 - y2 * x1)) / ((y3 - y4) * (x2 - x1) - (y1 - y2) * (x4 - x3))
    point_y = y1 + ((point_x - x1) * (y2 - y1)) / (x2 - x1)
    return np.array([point_x, point_y])

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def find_tangent_line(a, a_r):
    for i in range(0, 360):
        rotate_point = rotate(a, a_r, math.radians(i))
        
        L1 = line(a, rotate_point)
        
        if a[0] < rotate_point[0]:
            x_t = np.linspace(-50, 50, 500)
        else:
            x_t = np.linspace(50, -50, 500)

        y_t = (L1[2] - (L1[0] * x_t)) / (L1[1] + 0.0001)
        # plt.plot(x_t, y_t)
        # plt.plot(a[0],a[1], marker=".", markersize=15, color='red')
        # plt.plot([a[0], rotate_point[0]], [a[1], rotate_point[1]], marker=".", markersize=10, color='blue')
        
        poly_line = [[x, y] for x, y in zip(x_t, y_t)]

        rotate_line = LineString(poly_line)
        points = polygon.intersection(rotate_line)
        points = np.array(points.coords)
        # print(points)
        if len(points) == 2:
            # print("less")
            # idx = 0
            # plt.plot(points[idx, 0],points[idx, 1], marker=".", markersize=5, color='red')
            # plt.plot(points[-1, 0],points[-1, 1], marker=".", markersize=5, color='green')
            # plt.plot(x_t, y_t)
            
            return rotate_line
            # plt.plot([points[0, 0],points[-1, 0]], [points[0, 1],points[-1, 1]], marker=".", markersize=10, color='blue')


def quadratic_intersections(p, q):
    """Given two quadratics p and q, determines the points of intersection"""
    x = np.roots(np.asarray(p) - np.asarray(q))
    y = np.polyval(p, x)
    return x, y

def find_nearest(array, value):
    # array = np.asarray(array)
    # idx = (np.abs(array - value)).argmin()
    # return array[idx]
    return array[spatial.KDTree(array).query(value)[1]]

def calc_wurf(A, C, P, B, is_round=True):
    a = np.linalg.norm(A-C)
    b = np.linalg.norm(C-P)
    c = np.linalg.norm(P-B)
    w = ((a + b) * (b + c)) / (b * (a + b + c))
    # print(round(w,0))
    return round(w, 0) if is_round else w

def findValue(numbers, number_to_find, low, high, A, P, B):
	if high >= low:
		middle = low + (high - low) // 2
		if calc_wurf(A, numbers[middle], P, B) == number_to_find:
			return middle
		elif calc_wurf(A, numbers[middle], P, B) < number_to_find:
			return findValue(numbers, number_to_find, middle + 1, high,  A, P, B)
		else:
			return findValue(numbers, number_to_find, low, middle - 1,  A, P, B)
	
	else:
		return -1
# the parametric equation of an ellipse:
# x = u + a cos(t) ; y = v + b sin(t)

o1_x = 0.5    # x-position of 1 fig
o1_y = 0.3    # y-position of 1 fig

o2_x = -0.5   # x-position of 2 fig
o2_y = 0.3    # y-position of 2 fig

project_point1 = np.array([o1_x, o1_y, 1])
project_point2 = np.array([o2_x, o2_y, 1])

a = 3.     # radius on the x-axis
b = 5.     # radius on the y-axis

t = np.linspace(0, 2*pi, 200)

x = a * np.cos(t)
y = b * np.sin(t)

# ======================================
# fig = plt.figure(1)

# ax = plt.gca()
# ax.set_xlim([-5, 5])
# ax.set_ylim([-5, 5])

# plt.title("Овал")
# plt.plot(o1_x ,o1_y, marker=".", markersize=10)
# plt.plot(o2_x ,o2_y, marker=".", markersize=10)
# plt.plot(x ,y)
# plt.grid(color='lightgray',linestyle='--')
# # plt.axis("off")
# plt.box(False)

# ======================================
np.random.seed(2)
H = np.random.rand(3, 3)
H[-1,-1] = 1.

oval = np.stack((x, y, np.ones(x.shape[0])))
oval = H @ oval
project_point1 = H @ project_point1

fig = plt.figure(2)
# ax = fig.add_axes([0,0,1,1])
ax = plt.gca()
ax.set_xlim([-5, 5])
ax.set_ylim([-5, 5])

plt.grid(color='lightgray',linestyle='--')
# plt.axis("off")

plt.title("O1T")
plt.plot(project_point1[0], project_point1[1], marker=".", markersize=10, color='orange')
plt.plot(oval[0,:], oval[1,:])

# # ========================================
# np.random.seed(23)
# H = np.random.rand(3, 3)
# H[-1,-1] = 1.

# oval = np.stack((x, y, np.ones(x.shape[0])))
# oval = H @ oval
# project_point2 = H @ project_point2

# fig = plt.figure(3)

# plt.grid(color='lightgray',linestyle='--')
# # plt.axis("off")
# plt.title("O2")
# plt.plot(project_point2[0], project_point2[1], marker=".", markersize=10)
# plt.plot(oval[0,:], oval[1,:])
# # ========================================

oval = oval[:2, :]
poly = [[x, y] for x, y in zip(oval[0, :], oval[1,:])]

# i = 70
polygon = Polygon(poly)

count = 0
for i in range(oval.shape[1]):

    x_t, y_t = get_line_by_points(project_point1, oval[:2, i])
    # plt.plot(x_t, y_t)
    poly_line = [[x, y] for x, y in zip(x_t, y_t)]

    # line = [project_point1[:2], oval[:2, 70]]
    # shapely_line = LineString(line)

    
    path = LineString(poly_line)
    points = polygon.intersection(path)
    points = np.array(points.coords)
    
    # plt.plot(points[0, 0],points[0, 1], marker=".", markersize=5, color='red')
    # plt.plot(points[-1, 0],points[-1, 1], marker=".", markersize=5, color='green')
    
    a = (points[0, 0], points[0, 1])

    # b = (points[-1, 0], points[-1, 1])

    plt.plot(a[0], a[1], marker=".", markersize=15, color='green')
    point = (x[0]-5, y[0]-5)
    deg = 360
    p = rotate(a, point, deg)
    plt.plot(p[0], p[1], marker=".", markersize=15, color='green')
    xt, yt = get_line_by_points(a, p)

    line_rotate = [[x, y] for x, y in zip(xt, yt)]

    polygon = Polygon(poly)

    line_rotate = LineString(line_rotate)
    points = polygon.intersection(line_rotate)

    intersection_coords = np.array(points.coords)

    while len(intersection_coords) != 2:
        print(deg, len(intersection_coords))
        # if deg == 0.0:
        #     deg += 5
        if len(intersection_coords) == 0:
            deg *= 2
            p = rotate(a, point, deg)

            xt, yt = get_line_by_points(a, p)
            line_rotate = [[x, y] for x, y in zip(xt, yt)]
            line_rotate = LineString(line_rotate)
            points = polygon.intersection(line_rotate)
            intersection_coords = np.array(points.coords)

        elif len(intersection_coords) > 2:
            deg /= 2
            p = rotate(a, point, deg)
            
            xt, yt = get_line_by_points(a, p)
            line_rotate = [[x, y] for x, y in zip(xt, yt)]
            line_rotate = LineString(line_rotate)
            points = polygon.intersection(line_rotate)
            intersection_coords = np.array(points.coords)


    plt.plot(xt, yt)
    

    break

# draw line by two points 
# plt.plot([points[0, 0],points[-1, 0]], [points[0, 1],points[-1, 1]], marker=".", markersize=10, color='blue')
plt.show()
