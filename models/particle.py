### Definition of Particle
import numpy as np
import random

class Particle:
    def __init__(self, direction=None, position=None):
        if position is None:
            position = np.array((0,0,0), dtype=float)
        self.position = np.array(position, dtype=float)

        if direction is None:
            direction = self.generate_direction()
        self.direction = np.array(direction, dtype=float)
        self.direction /= np.linalg.norm(self.direction)

    def generate_direction(self):
        vec = np.random.normal(0, 1, 3)
        while vec[2] <= 0:
            vec = np.random.normal(0, 1, 3)
        return vec

    def position_t(self, t):
        return self.position + t * self.direction
    
    def __repr__(self):
        return f"Particle(position={self.position}, direction={self.direction})"

    def __str__(self):
        return f"Particle(position={self.position}, direction={self.direction})"




class LLParticle(Particle):
    """Decay in to two particles after a certain time"""

    def __init__(self, direction=None, position=None, decay_time=None, daughters=2):
        super().__init__(direction, position)

        # if no set decay time, set a random decay time (10-20?)
        if decay_time is None:
            decay_time = random.randint(10,20)

        self.decay_time = decay_time
        self.daughters = daughters

    def decay(self):
        decay_point = self.position_t(self.decay_time)

        """ Direction of two decay products"""
        rand_dir = np.random.normal(0, 1, 3)
        rand_dir /= np.linalg.norm(rand_dir)
        d1_local = rand_dir
        d2_local = -rand_dir

        d1 = d1_local + self.direction
        d2 = d2_local + self.direction

        d1 /= np.linalg.norm(d1)
        d2 /= np.linalg.norm(d2)

        return Particle(d1, decay_point), Particle(d2, decay_point)

    def __repr__(self):
        return f"Particle(position={self.position}, direction={self.direction}), Decay time={self.decay_time}, Decay at={self.position_t(self.decay_time)}"

    def __str__(self):
        return f"Particle(position={self.position}, direction={self.direction}), Decay time={self.decay_time}, Decay at={self.position_t(self.decay_time)}\n Decay Product1 direction={self.decay()[0].direction}, Decay Product2 direction={self.decay()[1].direction}"