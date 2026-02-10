import pygame, random, math

class Zombie:
    def __init__(self, width, height, base_speed, image_path):
        # Load and scale base zombie
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

        # --- Zombie Types ---
        zombie_type = random.choice(["normal", "fast", "tank"])
        if zombie_type == "normal":
            self.speed = base_speed
            self.health = 2
        elif zombie_type == "fast":
            self.speed = base_speed * 1.5
            self.health = 1
        else:  # tank
            self.speed = base_speed * 0.7
            self.health = 4

        self.type = zombie_type
        self.distance_to_player = float("inf")
        self.dash_cooldown = random.randint(120, 240)  # frames until next dash
        self.is_dashing = False
        self.dash_timer = 0

    def move_towards_player(self, player):
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        self.distance_to_player = distance

        if distance != 0:
            dx, dy = dx / distance, dy / distance  # normalize

            # --- Dash Mechanic ---
            if self.dash_cooldown <= 0 and not self.is_dashing and random.random() < 0.01:
                self.is_dashing = True
                self.dash_timer = 30  # dash lasts 30 frames
                self.dash_cooldown = random.randint(180, 300)  # cooldown

            if self.is_dashing:
                self.rect.x += dx * self.speed * 3
                self.rect.y += dy * self.speed * 3
                self.dash_timer -= 1
                if self.dash_timer <= 0:
                    self.is_dashing = False
            else:
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
                self.dash_cooldown -= 1

        # Rotate zombie to face player
        angle = math.degrees(math.atan2(-(player.rect.centery - self.rect.centery),
                                        (player.rect.centerx - self.rect.centerx)))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, win):
        # --- Glow effect that scales with distance ---
        if self.distance_to_player < 200:  
            glow_size = 12
            intensity = max(50, 200 - int(self.distance_to_player))  # closer = stronger glow
            glow_img = pygame.Surface(
                (self.rect.width + glow_size*2, self.rect.height + glow_size*2),
                pygame.SRCALPHA
            )
            color = (255, 0, 0, intensity) if self.type != "tank" else (255, 140, 0, intensity)
            pygame.draw.ellipse(glow_img, color, glow_img.get_rect())
            win.blit(glow_img, (self.rect.x - glow_size, self.rect.y - glow_size))

        # Draw zombie
        win.blit(self.image, self.rect)
