## To Evaluate the Result
import numpy as np


def get_points(detectors, position, direction, begin_z=0, end_z=1000):
    """ Get the coordinate with z same as detector """
    """ Input: detectors construction -> to get z coorinates, the position and direction of Fitting Result """

    C =[]
    z_layers = sorted(set(d.position[2] for d in detectors))
    for z in z_layers:
        if begin_z > z:
            continue
        if end_z < z:
            continue
        t = (z - position[2]) / direction[2]
        point = position + direction * t
        C.append(point)

    return np.array(C)



def angular_deviation(truth_direction, fit_direction):
    """ Get the different in angular """
    """ Input:  Truth direction and Fit Direction"""
    """ This way only considered track angular, not included initial points """

    v1 = fit_direction / np.linalg.norm(fit_direction)
    v2 = truth_direction / np.linalg.norm(truth_direction)
    cos_theta = np.clip(np.dot(v1, v2), -1.0, 1.0)

    print(f"Angular Deviation: {np.arccos(cos_theta)}")

    return np.arccos(cos_theta)



def compute_rmse(truth, fit):
    """ Get RMSE """
    """ Input: Truth interaction(with detector) data, and Fit interaction data """

    truth = np.array(truth)
    fit = np.array(fit)

    truth_dict = {z: xyz for *xyz, z in truth}
    fit_dict = {z: xyz for *xyz, z in fit}

    truth_dict = {row[2]: row[:3] for row in truth}
    fit_dict = {row[2]: row[:3] for row in fit}

    errors = []
    for z in fit_dict:
        if z in truth_dict:
            diff = np.array(fit_dict[z]) - np.array(truth_dict[z])
            errors.append(np.sum(diff**2))

    if not errors:
        print("No matched points!")
        return None

    rmse = np.sqrt(np.mean(errors)).item()
    print(f"RMSE: {rmse:.2f}")

    return rmse