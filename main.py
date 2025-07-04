import numpy as np
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from config.detector_config import detectors
import models.detector as de
from models.particle import Particle
import utils.fit_utils as fit_utils
import utils.data_io as data_io
import utils.evaluation as evaluation
from config.plot_config import *
import draw_detector


def main(particle, detectors, filename):
    hit_detectors = [d for d in detectors if d.is_hit(particle)]
    hit_count = len(hit_detectors)

    #if hit_count <= 1:
    #    return 0

    fig = plt.figure(1, figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    configure_plot(ax)
    for d in detectors:
        z = d.position[2]
        color = get_color_by_z(z)
        if d in hit_detectors:
            pass
        else:
            d.plot(ax, color=color)
    for d in hit_detectors:
        z = d.position[2]
        color = get_color_by_z(z)
        d.plot(ax, color=color)
        d.interaction_point(ax, particle)
    Final_Point = particle.position_t(200)
    # set high zorder value to make the track line drawn on top of all Detector Module
    #ax.plot([P1.position[0], Final_Point[0]], [P1.position[1],Final_Point[1]],[P1.position[2],Final_Point[2]], color="black", zorder=999)
    data_io.save_detected_data(detectors=detectors, particles=particle)
    data_io.save_truth_data(detectors, particle)

    plt.close()

    detector_data = pd.read_csv('data/detectors.csv')
    truth_data = pd.read_csv('data/particle.csv')
    points = detector_data[['x', 'y', 'z']].values
    track = truth_data[['x', 'y', 'z']].values
    px, py, pz = points.T
    tx, ty, tz = track.T


    t_vals = np.linspace(0, 200, 200)

    # =====Linear Fit=====
    initial, direction, init_point = fit_utils.Linear_Fit(points)
    line_points = init_point + t_vals[:, np.newaxis] * direction

    ang = evaluation.angular_deviation(particle.direction, direction)
    RMSE = evaluation.compute_rmse(track, evaluation.get_points(detectors, initial, direction))


    # =====Plotting=====
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    configure_plot(ax)

    for d in detectors:
        z = d.position[2]
        color = get_color_by_z(z)
        if d in hit_detectors:
            pass
        else:
            d.plot(ax, color=color)


    for d in hit_detectors:
        z = d.position[2]
        color = get_color_by_z(z)
        d.plot(ax, color=color)
        d.interaction_point(ax, P1)

    ax.scatter(px, py, pz, c='r', s=10, label='Detector Hit', marker='o', alpha=0.3)
    ax.scatter(tx, ty, tz, c='b', s=10, label='Truth Hit', marker='o', alpha=0.3)
    ax.plot(tx, ty, tz, c='b', label='Truth Track', alpha=0.3, zorder=500)
    ax.plot(line_points[:, 0], line_points[:, 1], line_points[:, 2], c='g', label='Least Fitted Track', alpha=0.3, zorder=499)
    ax.scatter(init_point[0], init_point[1], init_point[2], c='g', s=10)

    ax.legend()

    if os.path.exists(filename):
        id = len(pd.read_csv(filename))  + 1
        plt.savefig(f"Save1/fitting_{id}.png") 
    else:
        plt.savefig(f"Save1/fitting_1.png") 

    plt.close()

    df = pd.DataFrame({
    'dir_x': [particle.direction[0]],
    'dir_y': [particle.direction[1]],
    'dir_z': [particle.direction[2]],
    'hit_count': [hit_count],
    'Linear_dir_x': [direction[0]],
    'Linear_dir_y': [direction[1]],
    'Linear_dir_z': [direction[2]],
    'Linear_init_x': [init_point[0]],
    'Linear_init_y': [init_point[1]],
    'Linear_angle': [ang],
    'Linear_RMSE': [RMSE]
    })

    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    for d in detectors:
        d.clear()



folder_path = 'Save1/'
if os.path.exists(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith(('.png', '.csv')):
            os.remove(file_path)


for i in range(0,10):
    P1 = Particle()
    main(P1, detectors, 'Save1/particle_info.csv')

particle_info = pd.read_csv('Save1/particle_info.csv')
RMSES = particle_info['Linear_RMSE'].values

mean_rmse = np.mean(RMSES)
median_rmse = np.median(RMSES)
std_rmse = np.std(RMSES)

print(f"Mean RMSE: {mean_rmse}")
print(f"Median RMSE: {median_rmse}")
print(f"Standard Deviation of RMSE: {std_rmse}")
