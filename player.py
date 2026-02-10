import pygame, math, time

class Player:
    def __init__(self, x, y, speed, image_path):
        # Load and scale player bigger (80x80)
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (80, 80))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        # Movement & health
        self.speed = speed
        self.health = 3
        self.max_health = 3

        # --- Dash ability ---
        self.is_dashing = False
        self.dash_speed = 20
        self.dash_cooldown = 2  # seconds
        self.last_dash = 0

        # --- Weapons ---
        self.weapons = ["pistol", "shotgun", "rifle"]
        self.current_weapon = 0  # index in weapons list

        # --- XP & Leveling ---
        self.xp = 0
        self.level = 1
        self.xp_to_next = 10

        # --- Shield (power-up) ---
        self.shield = False
        self.shield_end_time = 0

    def handle_movement(self, keys, width, height):
        # Normal movement
        move_x, move_y = 0, 0
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:
            move_y -= self.speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < height:
            move_y += self.speed
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
            move_x -= self.speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < width:
            move_x += self.speed

        # Dash (Shift key)
        if keys[pygame.K_LSHIFT] and time.time() - self.last_dash > self.dash_cooldown:
            self.is_dashing = True
            self.last_dash = time.time()

        if self.is_dashing:
            move_x *= self.dash_speed
            move_y *= self.dash_speed
            self.is_dashing = False  # dash happens once per press

        self.rect.x += move_x
        self.rect.y += move_y

    def rotate_towards_mouse(self):
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.rect.centerx, my - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def switch_weapon(self, direction):
        """Switch weapons with mouse wheel or number keys"""
        self.current_weapon = (self.current_weapon + direction) % len(self.weapons)

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_to_next:
            self.level += 1
            self.xp = 0
            self.xp_to_next += 10
            self.max_health += 1
            self.health = self.max_health

    def activate_shield(self, duration=5):
        self.shield = True
        self.shield_end_time = time.time() + duration

    def update(self):
        # Check if shield expired
        if self.shield and time.time() > self.shield_end_time:
            self.shield = False

    def draw(self, win):
        self.rotate_towards_mouse()

        # Glow
        glow_size = 8
        glow_img = pygame.Surface(
            (self.rect.width + glow_size*2, self.rect.height + glow_size*2),
            pygame.SRCALPHA
        )
        pygame.draw.ellipse(glow_img, (255, 255, 255, 100), glow_img.get_rect())
        win.blit(glow_img, (self.rect.x - glow_size, self.rect.y - glow_size))

        # Health circle
        health_ratio = self.health / self.max_health
        radius = self.rect.width // 2 + 15
        center = self.rect.center

        pygame.draw.circle(win, (80, 80, 80), center, radius, 4)
        if self.health > self.max_health * 0.6:
            color = (0, 255, 0)
        elif self.health > self.max_health * 0.3:
            color = (255, 215, 0)
        else:
            color = (255, 0, 0)

        start_angle, end_angle = -90, -90 + 360 * health_ratio
        pygame.draw.arc(
            win, color,
            (center[0] - radius, center[1] - radius, radius*2, radius*2),
            math.radians(start_angle),
            math.radians(end_angle), 6
        )

        # Draw player
        win.blit(self.image, self.rect)

        # Shield indicator
        if self.shield:
            pygame.draw.circle(win, (0, 200, 255, 120), center, radius+10, 4)
