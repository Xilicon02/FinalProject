import numpy as np
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

from config.detector_config import detectors
import models.detector as de
from models.particle import Particle, LLParticle
import utils.fit_utils as fit_utils
import utils.data_io as data_io
import utils.evaluation as evaluation
from config.plot_config import *
import utils.draw_detector



def decay_case(particle, detectors, filename):
    if not isinstance(particle, LLParticle):
        raise ValueError("This case is used for particle decay")
    
    # A Mother particle and two Decay Products
    Mother = particle
    Product1, Product2 = Mother.decay()

    # 3 Particles hit detectors
    hit_detectors1 = [d for d in detectors if d.is_hit(Mother)]
    hit_detectors2 = [d for d in detectors if d.is_hit(Product1)]
    hit_detectors3 = [d for d in detectors if d.is_hit(Product2)]
    

    fig = plt.figure(1, figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    configure_plot(ax)

    for d in detectors:
        #d.clear()
        z = d.position[2]
        color = get_color_by_z(z)
        if d not in hit_detectors1 and d not in hit_detectors2 and d not in hit_detectors3:
            d.plot(ax, color=color)

    plot_hit_detectors(ax, hit_detectors1, Mother)
    plot_hit_detectors(ax, hit_detectors2, Product1)
    plot_hit_detectors(ax, hit_detectors3, Product2)

    #decay_time = Mother.decay_time
    #decay_point = Mother.position_t(decay_time)
    decay_point = Mother.end()

    data_io.save_detected_data(detectors, [Mother, Product1, Product2])
    data_io.save_truth_data(detectors, [Mother, Product1, Product2])

    plt.close()


    # =====Read Data=====
    detector_data = pd.read_csv('data/detectors.csv')
    truth_data = pd.read_csv('data/particle.csv')

    recorded = detector_data[['x', 'y', 'z', 'particle id']].values
    truth = truth_data[['x', 'y', 'z', 'particle id']].values
    rx, ry, rz ,ri = recorded.T
    tx, ty, tz, ti = truth.T


    # =====Separate Particle=====
    labels1 = truth[:,3]
    labels2 = recorded[:,3]
    truth_particles, recorded_particles = {}, {}
    for i in range(1,4):
        truth_particles[i] = truth[labels1==i][:,:3]
        recorded_particles[i] = recorded[labels2==i][:,:3]


    # =====Fitting=====
    initials, directions, init_points, rmses, xyzs = {}, {}, {}, {}, {}
    Ps = {1: Mother, 2: Product1, 3:Product2}

    for i in range(1,4):
        initials[i], directions[i], init_points[i] = fit_utils.Linear_Fit(recorded_particles[i])
        evaluation.angular_deviation(Ps[i].direction, directions[i])

        if i == 1:
            rmses[i] = evaluation.compute_rmse(truth_particles[i], evaluation.get_points(detectors, initials[i], directions[i], end_z=decay_point[2]))
        else:
            rmses[i] = evaluation.compute_rmse(truth_particles[i], evaluation.get_points(detectors, initials[i], directions[i], begin_z=decay_point[2]))

        zs = [truth_particles[i][:, 2].min(), truth_particles[i][:, 2].max()]
        xs = init_points[i][0] + (zs - init_points[i][2]) * directions[i][0] / directions[i][2]
        ys = init_points[i][1] + (zs - init_points[i][2]) * directions[i][1] / directions[i][2]
        xyzs[i] = (xs, ys, zs)

        truth_particles[i] = np.vstack([truth_particles[i], decay_point])


    # =====Plotting=====
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    configure_plot(ax)

    for d in detectors:
        z = d.position[2]
        color = get_color_by_z(z)
        if d in hit_detectors1 or d in hit_detectors2 or d in hit_detectors3:
            pass
        else:
            d.plot(ax, color=color)

    plot_hit_detectors(ax, hit_detectors1, Mother)
    plot_hit_detectors(ax, hit_detectors2, Product1)
    plot_hit_detectors(ax, hit_detectors3, Product2)

    ax.scatter(tx, ty, tz, c='b', s=30, label='Truth Hit', marker='o', alpha=0.3)
    ax.scatter(rx, ry, rz, c='r', s=30, label='Recorded Hit', marker='o')
    ax.scatter(*decay_point, c='black', s=50, label='decay point', marker='x')

    colors = {1: 'blue', 2: 'green', 3: 'orange'}

    for i in range(1, 4):
        ax.plot(truth_particles[i][:, 0], truth_particles[i][:, 1], truth_particles[i][:, 2],
                color=colors[i], label=f'Particle {i} Track', alpha=0.2)
        xs, ys, zs = xyzs[i]
        ax.plot(xs, ys, zs, color=colors[i])
    ax.legend()

    if os.path.exists(filename):
        id = len(pd.read_csv(filename)) + 1
        plt.savefig(f"Save2/fitting_{id}.png")
    else:
        plt.savefig(f"Save2/fitting_1.png")


    if any(rmse is None or (isinstance(rmse, float) and math.isnan(rmse)) for rmse in rmses.values()):
        print("Found None or NaN in RMSEs, skipping this iteration.")
        return
    
    rmse_all = np.sqrt(sum(rmse**2 for rmse in rmses.values()))

    
    df = pd.DataFrame({
        'Mother RMSES': [rmses[1]],
        'Product1 RMSES': [rmses[2]],
        'Product2 RMSES': [rmses[3]],
        'RMSES': [rmse_all]
    })


    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)


# ==========
# A draw hit detectors function, not know where to put
def plot_hit_detectors(ax, hit_detectors, particle):
    for d in hit_detectors:
        z = d.position[2]
        color = get_color_by_z(z)
        d.plot(ax, color=color)
        d.interaction_point(ax, particle)



if __name__ == "__main__":
    folder_path = 'Save2/'
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.endswith(('.png', '.csv')):
                os.remove(file_path)


    for i in range(0,100):
        MotherParticle = LLParticle()
        decay_case(MotherParticle, detectors, 'Save2/particle_info.csv')
    
    particle_info = pd.read_csv('Save2/particle_info.csv')
    RMSES = particle_info['RMSES'].values

    mean_rmse = np.mean(RMSES)

    print(f"Mean RMSE: {mean_rmse}")