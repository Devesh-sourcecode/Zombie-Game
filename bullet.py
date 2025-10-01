import pygame, math

class Bullet:
    def __init__(self, x, y, angle, speed, image_path):
        # Load and resize bullet image
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (40, 16))  # bigger bullet

        # Yellow glow surface (same size as bullet, larger)
        glow_size = 20
        self.glow_base = pygame.Surface(
            (self.original_image.get_width() + glow_size,
             self.original_image.get_height() + glow_size),
            pygame.SRCALPHA
        )
        pygame.draw.ellipse(
            self.glow_base,
            (255, 255, 0, 120),  # semi-transparent yellow
            self.glow_base.get_rect()
        )

        # Store movement
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.glow = pygame.transform.rotate(self.glow_base, -angle)
        self.rect = self.image.get_rect(center=(x, y))

        self.dx = math.cos(math.radians(angle))
        self.dy = -math.sin(math.radians(angle))
        self.speed = speed

    def move(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

    def draw(self, win):
        # Center glow around bullet and rotate with it
        glow_rect = self.glow.get_rect(center=self.rect.center)
        win.blit(self.glow, glow_rect)

        # Draw bullet on top
        win.blit(self.image, self.rect)
