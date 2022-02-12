import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon, LineString

from skimage import transform
from scipy import spatial
from skimage.io import imshow, imread
from math import pi, atan2
from scipy.interpolate import make_interp_spline
from inters import line

import matplotlib.pyplot as plt
from skimage import transform


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

# the parametric equation of an ellipse:
# x = u + a cos(t) ; y = v + b sin(t)

o1_x = 0.5    # x-position of 1 fig
o1_y = 0.3    # y-position of 1 fig

o2_x = -0.5   # x-position of 2 fig
o2_y = 0.3    # y-position of 2 fig

project_point1 = np.array([o1_x, o1_y, 1])
project_point2 = np.array([o2_x, o2_y, 1])

a = 2.     # radius on the x-axis
b = 4.     # radius on the y-axis

t = np.linspace(0, 2*pi, 200)

x = a * np.cos(t)
y = b * np.sin(t)

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

np.random.seed(2)
H = np.random.rand(3, 3)
H[-1,-1] = 1.

oval = np.stack((x, y, np.ones(x.shape[0])))
oval = H @ oval
project_point1 = H @ project_point1

fig = plt.figure(2)
# ax = fig.add_axes([0,0,1,1])
ax = plt.gca()
ax.set_xlim([-3, 3])
ax.set_ylim([-3, 3])

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

harmonic_contour = []

edge_points = []

for i in range(oval.shape[1]):
    # plt.plot(oval[0, i], oval[1, i], marker=".", markersize=10, color='red')
    L1 = line(project_point1, oval[:2, i])
    
    if i < oval.shape[1] // 2:
        x_t = np.linspace(-5, 5, 500)
    else:
        x_t = np.linspace(5, -5, 500)

    y_t = (L1[2] - (L1[0] * x_t)) / L1[1]

    poly_line = [[x, y] for x, y in zip(x_t, y_t)]

    polygon = Polygon(poly)
    path = LineString(poly_line)
    points = polygon.intersection(path)
    points = np.array(points.coords)

    idx = 0
    # plt.axes().set_aspect('equal', 'datalim')
    # if i < oval.shape[1] // 2:
    plt.plot(points[idx, 0],points[idx, 1], marker=".", markersize=5, color='red')
    # plt.plot(points[-1, 0],points[-1, 1], marker=".", markersize=5, color='green')
    edge_points.append([points[idx], points[-1]])
    # else:
    #     # plt.plot(points[idx, 0],points[idx, 1], marker=".", markersize=5, color='green')
    #     plt.plot(points[-1, 0],points[-1, 1], marker=".", markersize=5, color='green')
    #     edge_points.append([points[-1], points[idx]])
    #     points = points[::-1]
    
    # plt.plot([points[0, 0],points[-1, 0]], [points[0, 1],points[-1, 1]], marker=".", markersize=10, color='blue')
    # ax[1].plot(x_t, y_t)


    A = edge_points[-1][0]
    B = edge_points[-1][1]
    P = project_point1[:2]

    min_w = []
    points = points[::-1]
    for C in points[1:-1, :]:
        a = np.linalg.norm(A-C)
        b = np.linalg.norm(C-P)
        c = np.linalg.norm(P-B)
        w = ((a + b) * (b + c)) / (b * (a + b + c))
        if round(w, 1) == 1.0:
            # print(w, round(w, 0))
            min_w.append(C)
            break
    
    if min_w:
        min_w_np = np.array(min_w)
        C = find_nearest(min_w_np, P)
        # min_w_np = min_w_np[min_w_np[:,1].argsort()][::-1]
        # C = min_w_np[0]

        # a = np.linalg.norm(A-C)
        # b = np.linalg.norm(C-P)
        # c = np.linalg.norm(P-B)
        # w = ((a + b) * (b + c)) / (b * (a + b + c))
        # print(w)

        harmonic_contour.append(C)
        plt.plot(C[0],C[1], marker=".", markersize=5, color='green')
        
# harmonic_contour = np.array(harmonic_contour)
# harmonic_contour = harmonic_contour[harmonic_contour[:,0].argsort()][::-1]
# plt.plot(harmonic_contour[:,0],harmonic_contour[:,1], marker=".", markersize=5, color='blue')

# coord = [[1,1], [2,1], [2,2], [1,2], [0.5,1.5]]

def getClockwiseAngle(p):
    angle = 0.0
    angle = -1 * atan2(p[0], -1 * p[1])
    return angle


harmonic_contour.append(harmonic_contour[0])
# harmonic_contour.sort(key=lambda c:atan2(c[0], c[1]))
harmonic_contour.sort(key=getClockwiseAngle)
xs, ys = zip(*harmonic_contour)
plt.plot(xs,ys) 

# L1 = line(project_point1, oval[:2, i])
    
# if i < oval.shape[1] // 2:
#     x_t = np.linspace(-5, 5, 500)
# else:
#     x_t = np.linspace(5, -5, 500)

# y_t = (L1[2] - (L1[0] * x_t)) / L1[1]
# poly_line = [[x, y] for x, y in zip(x_t, y_t)]
# polygon = Polygon(poly)
# path = LineString(poly_line)
# points = polygon.intersection(path)
# points = np.array(points.coords)

plt.show()