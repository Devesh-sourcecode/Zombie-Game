# weapons.py
import math, time
from bullet import Bullet
from game_config import BULLET_SPEED

class Weapon:
    def __init__(self, owner):
        self.owner = owner
        self.last_fire = 0

    def can_fire(self):
        return True

    def fire(self):
        return []

class Pistol(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.cooldown = 250  # ms

    def can_fire(self):
        return (time.time() * 1000 - self.last_fire) >= self.cooldown

    def fire(self):
        if not self.can_fire(): return []
        self.last_fire = time.time() * 1000
        mx, my = self.owner.get_aim_pos()
        angle = math.degrees(math.atan2(-(my - self.owner.rect.centery), (mx - self.owner.rect.centerx)))
        return [Bullet(self.owner.rect.centerx, self.owner.rect.centery, angle, BULLET_SPEED, "./assets/bullet.png", damage=1)]

class Shotgun(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.cooldown = 700
        self.pellets = 6
        self.spread = 18  # degrees

    def can_fire(self):
        return (time.time() * 1000 - self.last_fire) >= self.cooldown

    def fire(self):
        if not self.can_fire(): return []
        self.last_fire = time.time() * 1000
        mx, my = self.owner.get_aim_pos()
        base_angle = math.degrees(math.atan2(-(my - self.owner.rect.centery), (mx - self.owner.rect.centerx)))
        bullets = []
        for i in range(self.pellets):
            offset = (i - self.pellets//2) * (self.spread / self.pellets)
            angle = base_angle + offset
            bullets.append(Bullet(self.owner.rect.centerx, self.owner.rect.centery, angle, BULLET_SPEED*0.85, "./assets/bullet.png", damage=1))
        return bullets

class Rifle(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.cooldown = 120  # faster
    def can_fire(self):
        return (time.time() * 1000 - self.last_fire) >= self.cooldown
    def fire(self):
        if not self.can_fire(): return []
        self.last_fire = time.time() * 1000
        mx, my = self.owner.get_aim_pos()
        angle = math.degrees(math.atan2(-(my - self.owner.rect.centery), (mx - self.owner.rect.centerx)))
        return [Bullet(self.owner.rect.centerx, self.owner.rect.centery, angle, BULLET_SPEED * 1.6, "./assets/bullet.png", damage=2)]
