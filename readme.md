# 🧟 Zombie Shooter Game (Python + Pygame)

A fast-paced **top-down zombie survival shooter** built using **Python** and **Pygame**.  
Fight against endless waves of zombies, switch weapons, and survive as long as possible.

---

## 🎮 Features

- 🧍 Smooth player movement with dash ability  
- 🔫 Multiple weapons:
  - Pistol
  - Shotgun (spread bullets)
  - Rifle (high speed)
- 🧟 Different zombie types:
  - Walker (balanced)
  - Runner (fast)
  - Tank (high health)
- 🌊 Wave system with increasing difficulty
- 💥 Bullet glow & particle effects
- ❤️ Health system with level-up healing
- 🛡 Shield power-up ability
- 🔊 Sound effects & background music
- 💾 High score saving system
- ⏸ Pause system

---

## 🗂️ Project Structure

zombie_game/
│── main.py            # Main game loop
│── player.py          # Player mechanics
│── zombie.py          # Zombie AI & types
│── bullet.py          # Bullet logic
│── weapons.py         # Weapon system
│── waves.py           # Wave & spawn manager
│── effects.py         # Particle effects
│── pickups.py         # Power-ups (health/shield)
│── audio_manager.py   # Sound system
│── save_manager.py    # High score saving
│── game_config.py     # Game settings & constants
│── README.md          # Project documentation
│
└── assets/            # Sprites and sounds
│── player.png
│── zombie.png
│── zombie_fast.png
│── zombie_tank.png
│── bullet.png
│── background.png
│── bg-music.mp3

---

## ⚡ Controls

| Key | Action |
|-----|--------|
| **W / A / S / D** | Move |
| **Mouse Move** | Aim |
| **Left Click** | Shoot |
| **Shift** | Dash |
| **1 / 2 / 3** | Switch Weapons |
| **P** | Pause Game |
| **ESC** | Quit |

---

## 🛠️ Requirements

- Python **3.8+**
- Pygame

Install dependency:
pip install pygame

## ▶️ How to Run

1. Download or clone this repository.
2. Make sure the `assets/` folder contains required images and sounds.
3. Run:
python main.py

## 🚀 Future Improvements

* Boss zombie with special attacks
* Upgrade & skill system
* More weapons
* Multiple maps
* Multiplayer mode
* Controller support
* Smarter zombie AI pathfinding

---

## 👨‍💻 Author

Developed as a Python game development project for learning game architecture and OOP design.
