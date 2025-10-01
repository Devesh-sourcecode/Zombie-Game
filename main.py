import pygame, sys, math, random
from player import Player
from zombie import Zombie
from bullet import Bullet

# Game setup
pygame.init()
pygame.mixer.init()  # initialize mixer for sounds
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Zombie Shooter")

# Fonts
font = pygame.font.SysFont("Arial", 30)
title_font = pygame.font.SysFont("Arial", 100)
gameover_font = pygame.font.SysFont("Arial", 80)

# Background image
bg = pygame.image.load("./assets/background.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Load sounds
bg_music = pygame.mixer.Sound("./assets/bg-music.mp3")
bg_music.set_volume(0.5)
bg_music.play(loops=-1)  # loop background music

bullet_sound = pygame.mixer.Sound("./assets/bullet-sound.mp3")
bullet_sound.set_volume(0.7)

zombie_hit_sound = pygame.mixer.Sound("./assets/zombie-death.mp3")
zombie_hit_sound.set_volume(0.7)

player_damage_sound = pygame.mixer.Sound("./assets/player-damage.mp3")
player_damage_sound.set_volume(0.7)

# Game states
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_INSTRUCTIONS = "instructions"
STATE_GAME_OVER = "game_over"

state = STATE_MENU

# Game objects
player = Player(WIDTH//2, HEIGHT//2, 5, "./assets/player.png")
zombies = []
bullets = []
score = 0

# Zombie spawn event
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 2000)

# Buttons
quit_button = pygame.Rect(WIDTH - 150, 20, 120, 40)
pause_button = pygame.Rect(WIDTH - 300, 20, 120, 40)

clock = pygame.time.Clock()
running = True
game_over = False
paused = False

def draw_button(rect, text, color=(0, 100, 200)):
    pygame.draw.rect(win, color, rect, border_radius=8)
    txt = font.render(text, True, (255, 255, 255))
    win.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))


# Main loop
while running:
    clock.tick(60)

    if state == STATE_MENU:
        win.fill((30, 30, 30))
        title = title_font.render("Zombie Shooter", True, (0, 200, 0))
        win.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))

        start_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50)
        instr_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
        quit_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 60, 200, 50)

        draw_button(start_btn, "Start")
        draw_button(instr_btn, "Instructions")
        draw_button(quit_btn, "Quit", (200, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_btn.collidepoint(event.pos):
                    state = STATE_GAME
                    game_over = False
                    paused = False
                    player = Player(WIDTH//2, HEIGHT//2, 5, "./assets/player.png")
                    zombies = []
                    bullets = []
                    score = 0
                elif instr_btn.collidepoint(event.pos):
                    state = STATE_INSTRUCTIONS
                elif quit_btn.collidepoint(event.pos):
                    pygame.quit(); sys.exit()

    elif state == STATE_INSTRUCTIONS:
        win.fill((20, 20, 20))
        title = gameover_font.render("Instructions", True, (200, 200, 0))
        win.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        controls = [
            "W - Move Up",
            "S - Move Down",
            "A - Move Left",
            "D - Move Right",
            "Mouse - Aim & Shoot",
            "P - Pause / Resume",
            "R - Restart when Game Over",
            "ESC - Quit",
        ]

        for i, text in enumerate(controls):
            line = font.render(text, True, (255, 255, 255))
            win.blit(line, (WIDTH//2 - line.get_width()//2, 250 + i*40))

        back_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT - 120, 200, 50)
        draw_button(back_btn, "Back", (200, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(event.pos):
                    state = STATE_MENU

    elif state == STATE_GAME:
        if not game_over:
            win.blit(bg, (0, 0))  # background

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == SPAWN_EVENT and not paused:
                    zombies.append(Zombie(WIDTH, HEIGHT, 2, "./assets/zombie.png"))
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if quit_button.collidepoint(event.pos):
                        pygame.quit(); sys.exit()
                    elif pause_button.collidepoint(event.pos):
                        paused = not paused
                    elif not paused:
                        mx, my = pygame.mouse.get_pos()
                        dx, dy = mx - player.rect.centerx, my - player.rect.centery
                        angle = math.degrees(math.atan2(-dy, dx))
                        bullets.append(Bullet(player.rect.centerx, player.rect.centery, angle, 10, "./assets/bullet.png"))

                        # Play bullet sound
                        bullet_sound.play()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused

            if not paused:
                keys = pygame.key.get_pressed()
                player.handle_movement(keys, WIDTH, HEIGHT)

                for bullet in bullets[:]:
                    bullet.move()
                    if not (0 <= bullet.rect.x <= WIDTH and 0 <= bullet.rect.y <= HEIGHT):
                        bullets.remove(bullet)

                for zombie in zombies[:]:
                    zombie.move_towards_player(player)

                    # Player hit
                    if zombie.rect.colliderect(player.rect):
                        zombies.remove(zombie)
                        player.health -= 1
                        player_damage_sound.play()
                        if player.health <= 0:
                            game_over = True
                            state = STATE_GAME_OVER

                    # Bullet hit zombie
                    for bullet in bullets[:]:
                        if zombie.rect.colliderect(bullet.rect):
                            try:
                                zombies.remove(zombie)
                                bullets.remove(bullet)
                                score += 1
                                zombie_hit_sound.play()
                            except: pass
                            break

            # Draw game
            player.draw(win)
            for bullet in bullets: bullet.draw(win)
            for zombie in zombies: zombie.draw(win)

            score_text = font.render(f"Score: {score}", True, (255,255,255))
            health_text = font.render(f"Lives: {player.health}", True, (255, 255, 255))
            win.blit(score_text, (10, 10))
            win.blit(health_text, (10, 50))

            draw_button(quit_button, "Quit", (200, 0, 0))
            pause_label = "Resume" if paused else "Pause"
            draw_button(pause_button, pause_label, (0, 100, 200))

            if paused:
                overlay = gameover_font.render("PAUSED", True, (255, 255, 0))
                win.blit(overlay, (WIDTH//2 - overlay.get_width()//2, HEIGHT//2 - 100))

    elif state == STATE_GAME_OVER:
        win.fill((0, 0, 0))
        gameover_text = gameover_font.render("GAME OVER", True, (255, 0, 0))
        score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        restart_text = font.render("Press R to Restart or ESC to Quit", True, (200, 200, 200))

        win.blit(gameover_text, (WIDTH//2 - gameover_text.get_width()//2, HEIGHT//2 - 100))
        win.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        win.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_r:
                    state = STATE_GAME
                    game_over = False
                    paused = False
                    player = Player(WIDTH//2, HEIGHT//2, 5, "./assets/player.png")
                    zombies = []
                    bullets = []
                    score = 0

    pygame.display.update()
