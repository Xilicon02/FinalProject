# Saving data as csv

import csv

def save_detected_data(detectors, particle, filename='data/detectors.csv'):
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["x", "y", "z"])

        for det in detectors:
            if det.is_hit(particle):
                writer.writerow(det.position)



def save_truth_data(detectors, particle, filename='data/particle.csv'):
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["x", "y", "z"])

        pos0 = particle.position
        dir = particle.direction

        z_layers = sorted(set(d.position[2] for d in detectors))

        for z in z_layers:
            t = (z - pos0[2]) / dir[2]
            point = pos0 + t * dir
            writer.writerow(point)