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


def main(particle, detectors, filename):
    hit_detectors = [d for d in detectors if d.is_hit(particle)]
    hit_count = len(hit_detectors)

    if hit_count <= 1:
        return 0

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
    data_io.save_detected_data(detectors, particle)
    data_io.save_truth_data(detectors, particle)

    detector_data = pd.read_csv('data/detectors.csv')
    truth_data = pd.read_csv('data/particle.csv')
    points = detector_data[['x', 'y', 'z']].values
    track = truth_data[['x', 'y', 'z']].values
    x, y, z = points.T
    tx, ty, tz = track.T


    t_vals = np.linspace(0, 200, 200)
    # =====PCA Fit=====
    centroid, direction1, init_point1 = fit_utils.PCA_Fit(points)
    line_points1 = init_point1  + t_vals[:, np.newaxis] * direction1
    
    ang1 = evaluation.angular_deviation(particle.direction, direction1)
    RMSE1 = evaluation.compute_rmse(track, evaluation.get_points(detectors, centroid, direction1))


    # =====Linear Fit=====
    initial, direction2, init_point2 = fit_utils.Linear_Fit(points)
    line_points = init_point2 + t_vals[:, np.newaxis] * direction2

    ang2 = evaluation.angular_deviation(particle.direction, direction2)
    RMSE2 = evaluation.compute_rmse(track, evaluation.get_points(detectors, initial, direction2))

    df = pd.DataFrame({
    'dir_x': [particle.direction[0]],
    'dir_y': [particle.direction[1]],
    'dir_z': [particle.direction[2]],
    'hit_count': [hit_count],
    'PCA_dir_x': [direction1[0]],
    'PCA_dir_y': [direction1[1]],
    'PCA_dir_z': [direction1[2]],
    'PCA_init_x': [init_point1[0]],
    'PCA_init_y': [init_point1[1]],
    'PCA_angle': [ang1],
    'PCA_RMSE': [RMSE1],
    'Linear_dir_x': [direction2[0]],
    'Linear_dir_y': [direction2[1]],
    'Linear_dir_z': [direction2[2]],
    'Linear_init_x': [init_point2[0]],
    'Linear_init_y': [init_point2[1]],
    'Linear_angle': [ang2],
    'Linear_RMSE': [RMSE2]
    })

    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)


if os.path.exists('data/particle_info.csv'):
    os.remove('data/particle_info.csv')


for i in range(0,100):
    P1 = Particle()
    main(P1, detectors, 'data/particle_info.csv')