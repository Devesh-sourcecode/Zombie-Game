# pickups.py
import pygame, random

class Pickup:
    def __init__(self, x, y, kind="health"):
        self.kind = kind  # "health" or "ammo" or "shield"
        self.image = pygame.image.load(f"./assets/{kind}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (36,36))
        self.rect = self.image.get_rect(center=(x,y))
        self.lifetime = 15000  # ms
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, win):
        win.blit(self.image, self.rect)

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime
