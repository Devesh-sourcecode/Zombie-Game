# effects.py
import random, pygame

def spawn_blood(particles_list, pos, amount=8):
    for _ in range(amount):
        particles_list.append({
            "pos":[pos[0], pos[1]],
            "vel":[random.uniform(-3,3), random.uniform(-3,3)],
            "life": random.randint(300,800)
        })

def update_particles(particles, dt):
    for p in particles[:]:
        p["pos"][0] += p["vel"][0]
        p["pos"][1] += p["vel"][1]
        p["life"] -= dt
        if p["life"] <= 0:
            particles.remove(p)

def draw_particles(win, particles):
    for p in particles:
        r = max(1, int(p["life"]/200))
        pygame.draw.circle(win, (120, 0, 0), (int(p["pos"][0]), int(p["pos"][1])), r)
