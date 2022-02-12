import numpy as np
import matplotlib.pyplot as plt
import math

def calc_slope_of_ellipse(ellipse_pars, x, y):
    """
    calculates the slope of the tangent at point x,y, the point needs to be on the ellipse!
    :param ellipse_params: tuple of (x0,y0,a,b,phi): x0,y0 center of ellipse; a,b sem-axis of ellipse; phi tilt rel to x axis  
    :param x: x-coord where the slope will be calculated  
    :returns: the slope of the tangent 
    """
    (x0, y0, a, b, phi) = ellipse_pars

    # transform to non-rotated ellipse centered to origin
    x_rot = (x - x0)*math.cos(phi) - (y - y0)*math.sin(phi)
    y_rot = (x - x0)*math.sin(phi) + (y - y0)*math.cos(phi)
    # Ax + By = C
    tan_a = x_rot/a**2
    tan_b = y_rot/b**2
    #rotate tangent line back to angle of the rotated ellipse
    tan_a_r = tan_a*math.cos(phi) + tan_b*math.sin(phi)
    tan_b_r = tan_b*math.cos(phi) - tan_a*math.sin(phi)
    m_tan = - (tan_a_r / tan_b_r)

    return m_tan

# Example focii and sum-distance
a1 = 1
b1 = 2
a2 = 5
b2 = 7
c = 9

# Compute ellipse parameters
a = c / 2                                # Semimajor axis
x0 = (a1 + a2) / 2                       # Center x-value
y0 = (b1 + b2) / 2                       # Center y-value
f = np.sqrt((a1 - x0)**2 + (b1 - y0)**2)  # Distance from center to focus
b = np.sqrt(a**2 - f**2)                 # Semiminor axis
phi = np.arctan2((b2 - b1), (a2 - a1))   # Angle betw major axis and x-axis

# Parametric plot in t
resolution = 1000
t = np.linspace(0, 2*np.pi, resolution)
x = x0 + a * np.cos(t) * np.cos(phi) - b * np.sin(t) * np.sin(phi)
y = y0 + a * np.cos(t) * np.sin(phi) + b * np.sin(t) * np.cos(phi)

# Plot ellipse
plt.plot(x, y)

# Show focii
plt.plot(a1, b1, 'bo')
plt.plot(a2, b2, 'bo')

plt.plot(x[0],y[0], marker=".", markersize=5, color='red')
plt.plot(x[x.shape[0]//2],y[x.shape[0]//2], marker=".", markersize=5, color='red')

m_t_l = calc_slope_of_ellipse((x0, y0, a, b, phi), x[0], y[0])

img = cv2.line(img, (int(round(x_int_l - (y_int/m_t_l))), 0), (int(round(x_int_l + ((height - y_int)/m_t_l))), int(round(height))), (255,0,255), thickness=1, lineType=cv2.LINE_AA)
print(m_t_l)

plt.axis('equal')
plt.show()
