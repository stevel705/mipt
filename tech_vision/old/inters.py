# import numpy as np
# import matplotlib.pyplot as plt
# def quadratic_intersections(p, q):
#     """Given two quadratics p and q, determines the points of intersection"""
#     x = np.roots(np.asarray(p) - np.asarray(q))
#     y = np.polyval(p, x)
#     return x, y

# x = np.array([[0.12, 0.11, 0.1, 0.09, 0.08],
#               [0.13, 0.12, 0.11, 0.1, 0.09],
#               [0.15, 0.14, 0.12, 0.11, 0.1],
#               [0.17, 0.15, 0.14, 0.12, 0.11],
#               [0.19, 0.17, 0.16, 0.14, 0.12],
#               [0.22, 0.19, 0.17, 0.15, 0.13],
#               [0.24, 0.22, 0.19, 0.16, 0.14],
#               [0.27, 0.24, 0.21, 0.18, 0.15],
#               [0.29, 0.26, 0.22, 0.19, 0.16]])

# y = np.array([[71.64, 78.52, 84.91, 89.35, 97.58],
#               [66.28, 73.67, 79.87, 85.36, 93.24],
#               [61.48, 69.31, 75.36, 81.87, 89.35],
#               [57.61, 65.75, 71.7, 79.1, 86.13],
#               [55.12, 63.34, 69.32, 77.29, 83.88],
#               [54.58, 62.54, 68.7, 76.72, 82.92],
#               [56.58, 63.87, 70.3, 77.69, 83.53],
#               [61.67, 67.79, 74.41, 80.43, 85.86],
#               [70.08, 74.62, 80.93, 85.06, 89.84]])

# x1 = np.linspace(0, 0.4, 100)
# y1 = -100 * x1 + 100
# plt.figure(figsize = (7,7))
# plt.subplot(111)

# plt.plot(x1, y1, linestyle = '-.', linewidth = 0.5, color =  'black')
# for i in range(5):
#     x_val = np.linspace(x[0, i] - 0.05, x[-1, i] + 0.05, 100)
#     poly = np.polyfit(x[:, i], y[:, i], deg=2)
#     y_int  = np.polyval(poly, x_val)
#     plt.plot(x[:, i], y[:, i], linestyle = '', marker = 'o')
#     plt.plot(x_val, y_int, linestyle = ':', linewidth = 0.25, color =  'black')
#     ix = quadratic_intersections(poly, [0, -100, 100])
#     plt.scatter(*ix, marker='x', color='black', s=40, linewidth=2)

# plt.xlabel('X')
# plt.ylabel('Y')
# plt.xlim([0,.35])
# plt.ylim([40,110])
# plt.show()


# s = input()

# def count_avg_score_and_neud(s):
#     count_neud = s.count('2')
#     list_with_neud = [int(char) for char in s if char != "2"]
#     return [sum(list_with_neud) // len(list_with_neud), count_neud]

# print(*count_avg_score_and_neud(s),end="\n")


from shapely.geometry import Polygon, LineString, Point

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False

A = [-5, 13]
B = [3, -3]
# C = [1, 8]
# D = [2, 4]

# print(line_intersection((A,B), (C, D)))

L1 = line(A, B)
# L2 = line(C, D)

# print(L1)

# print(intersection(L1, L2))


# first_line = LineString(np.column_stack((x, f)))
# second_line = LineString(np.column_stack((x, g)))
# intersection = first_line.intersection(second_line)

# if intersection.geom_type == 'MultiPoint':
#     plt.plot(*LineString(intersection).xy, 'o')
# elif intersection.geom_type == 'Point':
#     plt.plot(*intersection.xy, 'o')




# import numpy as np
# import matplotlib.pyplot as plt
# from sympy import *
# x, y = symbols('x y')

# P = np.array([1.42165228, 1.20097961])


# a=2; b=1
# F = x**2/a**2+y**2/b**2-1
# Fx = F.diff(x)
# Fy = F.diff(y)
# x0 = 1.5 # x координата точки касания
# y0 = solve(F.subs(x,x0),y)[-1] # находим y координаты точек касания
#  # и выбираем последнюю из списка
# Fx0 = Fx.subs([(x,x0),(y,y0)]) # значение производной Fx в точке касания
# Fy0 = Fy.subs([(x,x0),(y,y0)]) # значение производной Fy в точке касания
# # создание numpy функций из символьных выражений
# Fun = lambdify((x,y), F, "numpy")
# Tan = lambdify((x,y), Fx0*(x-x0)+Fy0*(y-y0), "numpy")
# Norm = lambdify((x,y), Fx0*(y-y0)-Fy0*(x-x0), "numpy")

# print(Tan)
# # построение графиков эллипса, касательной и нормали
# t = np.linspace(-a,a,31)
# Xf,Yf = np.meshgrid(t,t)
# plt.figure()
# plt.contour(Xf, Yf, Fun(Xf,Yf), [0], linewidths=3,colors='b' )
# tx=np.linspace(x0-1.0,x0+1.0,21)

# y0=float(y0) # преобразование символьного значения в числовое
# ty=np.linspace(y0-1,y0+1,21)
# Xt,Yt=np.meshgrid(tx,ty)
# plt.contour(Xt, Yt, Tan(Xt,Yt), [0] , linewidths=2,colors='r' )
# # plt.contour(Xt, Yt, Norm(Xt,Yt), [0] , linewidths=2,colors='g' )
# #plt.gcf().gca().axis([-3,3,-3,3]);
# plt.gcf().gca().axis('equal');
# plt.gcf().set_facecolor('white')
# plt.show()