import pygame, math

class Player:
    def __init__(self, x, y, speed, image_path):
        # Load and scale player bigger (80x80 instead of 50x50)
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (80, 80))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.health = 3
        self.max_health = 3  # for scaling health bar

    def handle_movement(self, keys, width, height):
        # Vertical movement (WASD + Arrows)
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:
            self.rect.y -= self.speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < height:
            self.rect.y += self.speed

        # Horizontal movement
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < width:
            self.rect.x += self.speed

    def rotate_towards_mouse(self):
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.rect.centerx, my - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))  # negative dy because pygame y-axis is inverted
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, win):
        # Rotate player before drawing
        self.rotate_towards_mouse()

        # --- White glow effect ---
        glow_size = 8
        glow_img = pygame.Surface(
            (self.rect.width + glow_size*2, self.rect.height + glow_size*2), 
            pygame.SRCALPHA
        )
        pygame.draw.ellipse(
            glow_img,
            (255, 255, 255, 100),  # semi-transparent white
            glow_img.get_rect()
        )
        win.blit(glow_img, (self.rect.x - glow_size, self.rect.y - glow_size))

        # --- Health bar (circular) ---
        health_ratio = self.health / self.max_health
        radius = self.rect.width // 2 + 15
        center = self.rect.center

        # Draw background circle (grey)
        pygame.draw.circle(win, (80, 80, 80), center, radius, 4)

        # Draw health arc (green -> yellow -> red depending on health)
        if self.health == 3:
            color = (0, 255, 0)
        elif self.health == 2:
            color = (255, 215, 0)
        else:
            color = (255, 0, 0)

        start_angle = -90  # start from top
        end_angle = start_angle + 360 * health_ratio
        pygame.draw.arc(
            win,
            color,
            (center[0] - radius, center[1] - radius, radius*2, radius*2),
            math.radians(start_angle),
            math.radians(end_angle),
            6
        )

        # --- Draw player image last (on top of everything) ---
        win.blit(self.image, self.rect)
