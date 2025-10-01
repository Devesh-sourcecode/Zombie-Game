import pygame, random, math

class Zombie:
    def __init__(self, width, height, speed, image_path):
        # Make zombies bigger (70x70 instead of 40x40)
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (70, 70))
        self.image = self.original_image

        # Spawn from random edge
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self.rect = self.image.get_rect(center=(random.randint(0, width), 0))
        elif side == "bottom":
            self.rect = self.image.get_rect(center=(random.randint(0, width), height))
        elif side == "left":
            self.rect = self.image.get_rect(center=(0, random.randint(0, height)))
        else:
            self.rect = self.image.get_rect(center=(width, random.randint(0, height)))

        self.speed = speed
        self.distance_to_player = float("inf")  # track distance to player for glow

    def move_towards_player(self, player):
        # Calculate direction vector
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        self.distance_to_player = distance  # store distance for glow effect

        if distance != 0:
            dx, dy = dx / distance, dy / distance  # normalize
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        # Rotate zombie toward player
        angle = math.degrees(math.atan2(-(player.rect.centery - self.rect.centery), (player.rect.centerx - self.rect.centerx)))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, win):
        # --- Red glow if close to player ---
        if self.distance_to_player < 120:  # glow radius trigger
            glow_size = 10
            glow_img = pygame.Surface(
                (self.rect.width + glow_size*2, self.rect.height + glow_size*2),
                pygame.SRCALPHA
            )
            pygame.draw.ellipse(
                glow_img,
                (255, 0, 0, 120),  # semi-transparent red
                glow_img.get_rect()
            )
            win.blit(glow_img, (self.rect.x - glow_size, self.rect.y - glow_size))

        # Draw zombie on top
        win.blit(self.image, self.rect)
