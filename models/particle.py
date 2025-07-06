### Definition of Particle
import numpy as np
import random

class Particle:
    def __init__(self, direction=None, position=None, init_time=0, speed=5.0):
        if position is None:
            position = np.array((0,0,0), dtype=float)
        self.position = np.array(position, dtype=float)
        self.init_time = init_time
        self.speed = speed  # -> mainly affect the lifetime setting

        if direction is None:
            direction = self.generate_direction()
        self.direction = np.array(direction, dtype=float)
        self.direction /= np.linalg.norm(self.direction)

    def generate_direction(self, theta_max_deg=60):
        """
        Generate a random direction vector within a cone defined by theta_max_deg.
        default 60
        """
        theta_max = np.radians(theta_max_deg)
        u = np.random.uniform(np.cos(theta_max), 1)
        theta = np.arccos(u)
        phi = np.random.uniform(0, 2 * np.pi)

        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)

        return np.array([x, y, z])

        #vec = np.random.normal(0, 1, 3)
        #while vec[2] <= 0:
        #    vec = np.random.normal(0, 1, 3)
        #return vec

    def position_t(self, t):
        delta_t = t - self.init_time
        return self.position + self.speed * delta_t * self.direction
    
    def __repr__(self):
        return f"Particle(position={self.position}, direction={self.direction}), speed={self.speed}"

    def __str__(self):
        return self.__repr__()   




class LLParticle(Particle):
    """Decay in to two particles after a certain time"""

    def __init__(self, direction=None, position=None, speed=5.0, decay_time=None, daughters=2):
        super().__init__(direction, position)

        # if no set decay time, set a random decay time (10-20?)
        if decay_time is None:
            decay_time = random.uniform(5,10)

        self.decay_time = decay_time
        self.daughters = daughters

        self._decayed = False
        self.d1 = None
        self.d2 = None
        self.decay_point = None

    def decay(self):
        if self._decayed:
            return (
                Particle(self.d1, self.decay_point, self.decay_time, self.speed), 
                Particle(self.d2, self.decay_point, self.decay_time, self.speed)
            )

        self.decay_point = self.position_t(self.decay_time)

        """ Direction of two decay products"""
        rand_dir = np.random.normal(0, 1, 3)
        rand_dir /= np.linalg.norm(rand_dir)
        d1_local = rand_dir
        d2_local = -rand_dir

        d1 = d1_local + self.direction
        d2 = d2_local + self.direction

        d1 /= np.linalg.norm(d1)
        d2 /= np.linalg.norm(d2)

        self.d1 = d1
        self.d2 = d2
        self._decayed = True

        return (
            Particle(d1, self.decay_point, self.decay_time, self.speed), 
            Particle(d2, self.decay_point, self.decay_time, self.speed)
        )


    def end(self):
        x, y, z = self.position_t(self.decay_time)
        return np.array((x, y, z), dtype=float)


    def __repr__(self):
        if not self._decayed:
            self.decay()
        return (f"Particle(position={self.position}, direction={self.direction})\n"
                f"Decay time={self.decay_time}, Decay at={self.decay_point}\n"
                f"Decay Product1 direction={self.d1}\n"
                f"Decay Product2 direction={self.d2}")


    def __str__(self):
        return self.__repr__()