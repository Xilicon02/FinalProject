## Definition of Detector
import os
import sys
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from models.particle import LLParticle

class DetectorModule:

    def __init__(self, size, position):
        # Error case
        if size not in [25, 50, 100]:
            raise ValueError("Size must be one of [25, 50, 100]")
        if len(position) != 3:
            raise ValueError("Position must be 3D")
        
        self.size = size
        self.position = position
        self.was_hit = False
        self.hit_time = 0

        # set price
        if size == 100:
            self.price = 100
        elif size == 50:
            self.price = 35
        elif size == 25:
            self.price = 12


    # xmin, xmax, ymin, ymax, z
    def bounds(self):
        x, y, z = self.position
        half = self.size / 2
        return (x - half, x + half), (y - half, y + half), z


    # Whether hit by particle
    def is_hit(self, particle):
        if particle is None:
            return False
        
        (x_min, x_max), (y_min, y_max), z = self.bounds()

        pos0 = particle.position
        dir = particle.direction

        if dir[2] == 0:
            raise ValueError("track parallel to the x-y, no intersection")

        #if z >= pos0[2]:
        t = (z - pos0[2]) / (dir[2] * particle.speed)
        if t >= 0:
            inter_point = particle.position_t(t)
            x_int, y_int = inter_point[0], inter_point[1]
        
            # decay case
            if isinstance(particle, LLParticle):
                z_end = particle.end()[2]
                if z_end < z:
                    return False

            # on x_min, y_min or larger, x_max and y_max not included
            if (x_min <= x_int < x_max) and (y_min <= y_int < y_max):
                self.was_hit = True
                #print(t)
                x, y, z = particle.position_t(t)
                #if t not in self.hit_times:
                #    self.hit_times.append(t)
                self.hit_time = t + particle.init_time
                return True
            else:
                return False


    # Draw the interaction point
    def interaction_point(self, ax, particle):
        if self.is_hit(particle):
            z = self.bounds()[2]
            t = (z - particle.position[2]) / (particle.direction[2]*particle.speed)
            if t >= 0:
                inter_point = particle.position_t(t)
                x_int, y_int = inter_point[0], inter_point[1]
                ax.scatter(x_int, y_int, z, color='b', s=25)


    # Draw the detector module
    def plot(self, ax, color):
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection

        (x_min, x_max), (y_min, y_max), z = self.bounds()
        verts = [
            (x_min, y_min, z),
            (x_max, y_min, z),
            (x_max, y_max, z),
            (x_min, y_max, z),
        ]

        alpha = 0.7 if self.was_hit else 0.2
        # edgecolor='none' for no line in the edge
        square = Poly3DCollection([verts], color=color, alpha=alpha)
        #square = Poly3DCollection([verts], color=color, alpha=alpha, edgecolor='none')
        ax.add_collection3d(square)


    def clear(self):
        """Reset the hit status and time"""
        self.was_hit = False
        self.hit_time = 0


    def __repr__(self):
        return f"DetectorModule(size={self.size}cm, position={self.position}, price={self.price}万)"
        # 1万 = 10 thousand

    
    def __str__(self):
        return self.__repr__()




## Put detector function
########################### May have bug or can update
# x, y need to be n*size when setting, the center of detector module
# the midule one for each z is (x=0, y=0)
def Set_Detector_Module(size, x_range, y_range, z):
    detectors = []
    X, Y = np.meshgrid(np.arange(-x_range, x_range+1, size), np.arange(-y_range, y_range+1, size))
    for x, y in zip(X.flatten(), Y.flatten()):
        detectors.append(DetectorModule(size, (x, y, z)))
    return detectors




## Total Price
def Get_Price(detectors):
    price = 0

    if isinstance(detectors, DetectorModule):
        price = detectors.price
    elif isinstance(detectors, list):
        if len(detectors) == 0:
            print("No detectors to calculate price.")
            return 0
        for detector in detectors:
            price += detector.price
    else:
        raise TypeError("Unsupported input type for detectors: expected DetectorModule or list of them.")
    
    if price > 7200:
        print("Price exceeds budget of 7200: {}".format(price))
    else:
        print("Total price is within budget: {}".format(price))
    
    return price