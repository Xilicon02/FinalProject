### Definition of Particle
import numpy as np

class Particle:
    def __init__(self, direction, position=None):
        if position is None:
            position = np.array((0,0,0), dtype=float)
        self.position = np.array(position, dtype=float)
        self.direction = np.array(direction, dtype=float)
        self.direction /= np.linalg.norm(self.direction)

    def position_t(self, t):
        return self.position + t * self.direction