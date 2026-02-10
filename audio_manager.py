# audio_manager.py
import pygame, os

class AudioManager:
    def __init__(self):
        try:
            pygame.mixer.init()
        except Exception:
            pass
        self.sounds = {}
        self.music = None

    def load(self, key, path):
        if not os.path.isfile(path):
            print(f"[Audio] missing: {path}")
            return
        self.sounds[key] = pygame.mixer.Sound(path)

    def play(self, key, loops=0):
        s = self.sounds.get(key)
        if s:
            s.play(loops=loops)

    def set_volume(self, key, vol):
        s = self.sounds.get(key)
        if s: s.set_volume(vol)

    def play_music(self, path, loops=-1, volume=0.5):
        if not os.path.isfile(path):
            print(f"[Audio] music missing: {path}")
            return
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)
