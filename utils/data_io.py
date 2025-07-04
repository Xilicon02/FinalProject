# Saving data as csv
import csv
from models.detector import LLParticle


def save_detected_data(detectors, particles, filename='data/detectors.csv'):
    """
    save the detected data (center of hit detectors) to a CSV file.

    input
    - detectors: list of detectors, need particle
    - particle: particle object, need detectors
    - filename: CSV path
    """
    if not isinstance(particles, (list, tuple)):
        particles = [particles]

    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["x", "y", "z", "t"])

        for det in detectors:
            for p in particles:
                if det.is_hit(p):
                    writer.writerow([*det.position, det.hit_time])



def save_truth_data(detectors, particle, filename='data/particle.csv'):
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["x", "y", "z"])

        pos0 = particle.position
        dir = particle.direction

        z_layers = sorted(set(d.position[2] for d in detectors))

        for z in z_layers:
            if isinstance(particle, LLParticle):
                z_end = particle.end()[2]
                if z_end < z:
                    continue
            t = (z - pos0[2]) / dir[2]
            point = pos0 + t * dir
            writer.writerow(point)