# 🧟 Zombie Shooter Game (Python + Pygame)

A simple **top-down zombie shooter game** built with **Python** and **Pygame**.  
The player controls a character, shoots zombies, and tries to survive as long as possible.  

---

## 🎮 Features
- Player movement with **WASD keys**  
- Aim & shoot using the **mouse** (left-click to fire bullets)  
- Zombies spawn randomly and chase the player  
- Player has **3 lives**  
- Score increases when zombies are killed  
- Game ends when health reaches 0  

---

## 🗂️ Project Structure
zombie_game/
│── main.py # Main game loop
│── player.py # Player class
│── zombie.py # Zombie class
│── bullet.py # Bullet class
│── settings.py # (optional) constants for screen size, speed, colors
│── README.md # Project description
│
└── assets/ # Sprites and sounds
│── player.png
│── zombie.png
│── bullet.png
│── bg_music.mp3 (optional)
│── shoot.wav (optional)


---

## ⚡ Controls
- **WASD** → Move player  
- **Mouse Move** → Aim  
- **Left Click** → Shoot  

---

## 🛠️ Requirements
- Python **3.8+**  
- [Pygame](https://www.pygame.org/wiki/GettingStarted)  

Install dependencies:
```bash
pip install pygame


▶️ How to Run

Clone this repository or download the project folder.

Place your assets (player, zombie, bullet images) inside the assets/ folder.

Run the game:

python main.py


👨‍💻 Author
---

👉 You just need to create a new file in your folder called `README.md` and paste this content.  

Do you want me to also **create a `settings.py` file** (to keep screen size, colors, speeds, etc. in one place) so the game is easier to tweak later?
