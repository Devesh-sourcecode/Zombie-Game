# save_manager.py
import json, os

SAVE_FILE = "save.json"

def load_highscore():
    if not os.path.exists(SAVE_FILE):
        return 0
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            return data.get("highscore", 0)
    except:
        return 0

def save_highscore(score):
    data = {"highscore": score}
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
    except:
        pass
