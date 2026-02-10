# waves.py
import random, pygame
from zombie import Zombie

class WaveManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.wave = 1
        self.kills_this_wave = 0
        self.target_kills = 10
        self.spawn_interval = 2000
        self.spawn_timer = 0

    def next_wave(self):
        self.wave += 1
        self.kills_this_wave = 0
        self.target_kills = int(self.target_kills * 1.3)
        self.spawn_interval = max(400, int(self.spawn_interval * 0.9))

    def register_kill(self):
        self.kills_this_wave += 1
        if self.kills_this_wave >= self.target_kills:
            self.next_wave()
            return True
        return False

    def spawn_zombie(self):
        # decide type by wave
        r = random.random()
        if self.wave >= 6 and r < 0.05:
            ztype = "tank"
        elif r < 0.3:
            ztype = "runner"
        else:
            ztype = "walker"
        return Zombie(self.width, self.height, ztype)
