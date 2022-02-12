from warnings import catch_warnings
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon, LineString

from skimage import transform
from scipy import spatial
from skimage.io import imshow, imread
from math import fabs, pi, atan2
from scipy.interpolate import make_interp_spline
from inters import intersection, line
from tqdm import tqdm

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
b = 3.     # radius on the y-axis

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
# oval = list(oval)
# oval.sort(key=lambda c:atan2(c[0], c[1]))
# oval = np.array(oval)
# print(oval.shape)
poly = [[x, y] for x, y in zip(oval[0, :], oval[1,:])]

harmonic_contour = []

edge_points = []
res = None

for i in range(oval.shape[1]):
    # plt.plot(oval[0, i], oval[1, i], marker=".", markersize=10, color='red')
    L1 = line(project_point1, oval[:2, i])
    
    if project_point1[0] < oval[:2, i][0]:
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
    # plt.plot(points[idx, 0],points[idx, 1], marker=".", markersize=5, color='red')
    # plt.plot(points[-1, 0],points[-1, 1], marker=".", markersize=5, color='green')
    edge_points.append([points[idx], points[-1]])

    # plt.plot([points[0, 0],points[-1, 0]], [points[0, 1],points[-1, 1]], marker=".", markersize=10, color='blue')
    # break
    # ax[1].plot(x_t, y_t)

    A = edge_points[-1][0]
    B = edge_points[-1][1]
    P = project_point1[:2]

    L1 = line(A, P)

    x_t = np.linspace(A[0], P[0], 500)
    y_t = (L1[2] - (L1[0] * x_t)) / L1[1]
    
    poly_line = [[x, y] for x, y in zip(x_t, y_t)]
        
    if not res:
        res = findValue(poly_line, 1.0, 0, len(poly_line), A, P, B)

    harmonic_contour.append(poly_line[res])
    
    # plt.plot(poly_line[res][0], poly_line[res][1], marker=".", markersize=5, color='blue')
    

harmonic_contour.append(harmonic_contour[0])
xs, ys = zip(*harmonic_contour)
plt.plot(xs, ys) 

# =================================================
idx = 0
w1 = []
w2 = []

for i in tqdm(range(idx,len(edge_points))):
    L1 = line(edge_points[i][0], edge_points[i][1])
    if edge_points[i][0][0] < 0:
        x_t = np.linspace(edge_points[i][0][0], edge_points[i][1][0], 200)
    else:
        x_t = np.linspace(edge_points[i][1][0], edge_points[i][0][0], 200)

    y_t = (L1[2] - (L1[0] * x_t)) / L1[1]

    # plt.plot(x_t, y_t) 
    line_from_harmonic_wurf = [[x, y] for x, y in zip(x_t, y_t)]

    harmonic_contour_polygon = Polygon(harmonic_contour)
    path = LineString(line_from_harmonic_wurf)
    points_wurf = harmonic_contour_polygon.intersection(path)

    points = np.array(points_wurf.coords)
    # plt.plot(x_t, y_t, marker=".", markersize=5, color='black')
    # plt.plot([points[0, 0],points[-1, 0]], [points[0, 1],points[-1, 1]], marker=".", markersize=10, color='blue')
    # break

    A = edge_points[i][0]
    D = edge_points[i][1]
    B = points[0]
    C = points[-1]
    # plt.plot(A[0],A[1], marker=".", markersize=5, color='red')
    # plt.plot(D[0],D[1], marker=".", markersize=5, color='red')
    # plt.plot(B[0],B[1], marker=".", markersize=5, color='red')
    # plt.plot(C[0],C[1], marker=".", markersize=5, color='red')


    x_t = np.linspace(-30, 30, 100)

    prev = []
    tangent_points = set()
    for i in x_t:
        for j in x_t:
            tmp_point = [i, j]

            find_line = [[A[0],A[1]], [tmp_point[0],tmp_point[1]]]
            path = LineString(find_line)
            intersection_harmonic_wurf = harmonic_contour_polygon.intersection(path)
            points = np.array(intersection_harmonic_wurf.coords)

            if len(points) > 0:
                if len(prev) == 0:
                    tangent_points.add((points[0, 0], points[0, 1]))
                    # plt.plot(points[0, 0], points[0, 1], marker=".", markersize=10, color='blue')
                    
                prev = points
            else:
                if len(prev) > 0:
                    tangent_points.add((prev[0, 0], prev[0, 1]))
                    # plt.plot(prev[0, 0],prev[0, 1], marker=".", markersize=10, color='blue')
                    
            
            # if len(points) > 0:
            #     print(len(points))
    tangent_points = sorted(list(tangent_points), key=lambda x: x[1])
    # plt.plot([tangent_points[0][0], tangent_points[-1][0]], [tangent_points[0][1],tangent_points[-1][1]], marker=".", markersize=10, color='blue')
    # plt.plot([A[0],tmp_point[0]], [A[1], tmp_point[1]], marker=".", markersize=5, color='red')

    L1 = line(tangent_points[0], tangent_points[-1])

    if tangent_points[0][0] < 0:
        x_t = np.linspace(-5, 5, 200)
    else:
        x_t = np.linspace(5, -5, 200)

    y_t = (L1[2] - (L1[0] * x_t)) / L1[1]

    line_from_harmonic_wurf = [[x, y] for x, y in zip(x_t, y_t)]

    harmonic_contour_polygon = Polygon(poly)
    path = LineString(line_from_harmonic_wurf)
    points_wurf = harmonic_contour_polygon.intersection(path)

    points = np.array(points_wurf.coords)

    A_w1 = points[0]
    D_w1 = points[-1]
    B_w1 = np.array(tangent_points[0])
    C_w1 = np.array(tangent_points[-1])

    plt.plot(A_w1[0], A_w1[1], marker=".", markersize=5, color='red')
    plt.plot(D_w1[0], D_w1[1], marker=".", markersize=5, color='red')
    plt.plot(B_w1[0], B_w1[1], marker=".", markersize=5, color='red')
    plt.plot(C_w1[0], C_w1[1], marker=".", markersize=5, color='red')
    w1.append(calc_wurf(A_w1, B_w1, C_w1, D_w1, is_round=False))

    
    
    L1 = line(A_w1, D_w1)
    y_t = (L1[2] - (L1[0] * x_t)) / L1[1]
    line_from_harmonic_wurf = [[x, y] for x, y in zip(x_t, y_t)]
    w1_line = LineString(line_from_harmonic_wurf)


    plt.plot(*w1_line.xy, color='red')


    # W2 ===========================================
    ab = LineString([A, B])
    harmonic_contour_polygon = Polygon(harmonic_contour)
    points_wurf = harmonic_contour_polygon.intersection(ab)
    try:
        points = np.array(points_wurf.coords)
    except:
        w1.pop()
        continue
    # A = edge_points[i][0]
    
    if len(points) < 1:
        w1.pop()
        continue 

    B = points[0]
    C_w2 = points[-1]
    cd_length = 5

    edge_points_np = np.array(edge_points).reshape(-1, 2)
    nearest_point = find_nearest(edge_points_np, np.array(B))
    # plt.plot([D_w1[0], B[0]], [D_w1[1],B[1]], marker=".", markersize=10, color='green')
    # plt.plot(nearest_point[0], nearest_point[1], marker=".", markersize=15, color='black')
    
    # ab = LineString([D_w1, B])

    x_t = np.linspace(-5, 5, 200)
    # y_t = slope * x_t + intercept
    L1 = line(B, A_w1)
    y_t = (L1[2] - (L1[0] * x_t)) / L1[1]

    plt.plot(x_t, y_t) 
    line_w2_wurf = [[x, y] for x, y in zip(x_t, y_t)]

    # plt.plot(x_t, y_t, marker=".", markersize=5, color='black')
    w2_line = LineString(line_w2_wurf)
    # left = ab.parallel_offset(cd_length / 2, 'left')
    # right = ab.parallel_offset(cd_length / 2, 'right')
    # c = left.boundary[1]
    # d = right.boundary[0]  # note the different orientation for right offset
    # cd = LineString([c, d])
    
    # plt.plot([np.array(c)[0], np.array(d)[0]],[np.array(c)[1], np.array(d)[1]], marker=".", markersize=15, color='black')
    points_contour = w1_line.intersection(w2_line)
    points = np.array(points_contour.coords)

    if len(points) > 0:
        bound1 = points[0]
        # bound2 = points[-1]
        plt.plot(bound1[0],bound1[1], marker=".", markersize=10, color='blue')
        # plt.plot([points[0, 0],points[-1, 0]], [points[0, 1],points[-1, 1]], marker=".", markersize=10, color='blue')
        
    w2.append(calc_wurf(A_w1, B, C_w2, bound1))
    # break


fig = plt.figure(3)
plt.plot(w1, w2)


# plt.axis('equal')
plt.show()