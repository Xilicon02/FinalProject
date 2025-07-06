# Which one is better?
import numpy as np

def On_xyPlane(centroid, direction):
    zero = -centroid[2]/direction[2]
    x_zero = centroid[0] + zero * direction[0]
    y_zero = centroid[1] + zero * direction[1]
    z_zero = centroid[2] + zero * direction[2]
    init_point = np.array([x_zero, y_zero, z_zero])
    return init_point

def linear_fit(y):
    t = np.arange(y.shape[0])
    A = np.vstack([t, np.ones(len(t))]).T 
    params, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
    return params




#### Fitting Function

def PCA_Fit(data):
    """detector.csv as input, using PCA Method"""

    centroid = data.mean(axis=0)

    centered = data - centroid

    _, _, vh = np.linalg.svd(centered)
    direction = vh[0]
    if direction[2] < 0:
        direction *= -1

    init_point = On_xyPlane(centroid, direction)

    return centroid, direction, init_point





def Linear_Fit(data):
    """detector.csv as input, using Least Squares Fitting Method"""
    params_x = linear_fit(data[:, 0])
    params_y = linear_fit(data[:, 1])
    params_z = linear_fit(data[:, 2])

    direction = np.array([params_x[0], params_y[0], params_z[0]])
    direction /= np.linalg.norm(direction)

    initial = np.array([params_x[1], params_y[1], params_z[1]])

    init_point = On_xyPlane(initial, direction)

    return initial, direction, init_point