import pygame, math

class Bullet:
    def __init__(self, x, y, angle, speed, image_path, damage=1, piercing=False, lifetime=90):
        # Load and resize bullet image
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (45, 18))  # slightly bigger

        # Yellow glow surface (bigger than bullet)
        glow_size = 25
        self.glow_base = pygame.Surface(
            (self.original_image.get_width() + glow_size,
             self.original_image.get_height() + glow_size),
            pygame.SRCALPHA
        )
        pygame.draw.ellipse(
            self.glow_base,
            (255, 255, 120, 150),  # strong yellow glow
            self.glow_base.get_rect()
        )

        # Movement & rotation
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.glow = pygame.transform.rotate(self.glow_base, -angle)
        self.rect = self.image.get_rect(center=(x, y))

        # Direction vector
        self.dx = math.cos(math.radians(angle))
        self.dy = -math.sin(math.radians(angle))
        self.speed = speed

        # Gameplay properties
        self.damage = damage
        self.piercing = piercing
        self.lifetime = lifetime  # frames before disappearing

    def move(self):
        # Move bullet in direction
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        self.lifetime -= 1  # countdown lifetime

    def draw(self, win):
        # Sync glow with bullet rotation
        self.glow = pygame.transform.rotate(self.glow_base, -self.angle)
        glow_rect = self.glow.get_rect(center=self.rect.center)
        win.blit(self.glow, glow_rect)

        # Draw bullet
        win.blit(self.image, self.rect)

    def is_expired(self, width, height):
        """ Check if bullet should be removed """
        return (
            self.lifetime <= 0 or
            self.rect.right < 0 or self.rect.left > width or
            self.rect.bottom < 0 or self.rect.top > height
        )
