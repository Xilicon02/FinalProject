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

    #with open(filename, mode='w', newline='') as csvfile:
    #    writer = csv.writer(csvfile)
    #    writer.writerow(["x", "y", "z", "t"])
    #
    #    for det in detectors:
    #        for p in particles:
    #            if det.is_hit(p):
    #                writer.writerow([*det.position, det.hit_time])

    ## 我实在不知道该怎么区分不同粒子的轨迹了！！！！
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["x", "y", "z", "particle id"])

        for i in range(len(particles)):
            for det in detectors:
                if det.is_hit(particles[i]):
                    writer.writerow([*det.position, i+1])



def save_truth_data(detectors, particles, filename='data/particle.csv'):
    if not isinstance(particles, (list, tuple)):
        particles = [particles]
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["x", "y", "z", "particle id"])

        for i in range(len(particles)):
            pos0 = particles[i].position
            dir = particles[i].direction

            z_layers = sorted(set(d.position[2] for d in detectors))

            for z in z_layers:
                if pos0[2] > z:
                    continue
                if isinstance(particles[i], LLParticle):
                    z_end = particles[i].end()[2]
                    if z_end < z:
                        continue
                t = (z - pos0[2]) / dir[2]
                point = pos0 + t * dir
                writer.writerow([*point, i+1])


        #pos0 = particles.position
        #dir = particles.direction

        #z_layers = sorted(set(d.position[2] for d in detectors))

        #for z in z_layers:
        #    if isinstance(particles, LLParticle):
        #        z_end = particles.end()[2]
        #        if z_end < z:
        #            continue
        #    t = (z - pos0[2]) / dir[2] * particles
        #    point = pos0 + t * dir
        #    writer.writerow(point)