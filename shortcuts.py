import json
import re
import subprocess
from pathlib import Path
import sober

SHORTCUTS_FILE = Path.home() / ".local/Lution/game_shortcuts.json"


def load():
    if not SHORTCUTS_FILE.exists():
        return {}
    try:
        return json.loads(SHORTCUTS_FILE.read_text())
    except Exception:
        return {}


def save(shortcuts):
    SHORTCUTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SHORTCUTS_FILE.write_text(json.dumps(shortcuts, indent=2) + "\n")


def add(name, place_id):
    s = load()
    s[name.strip()] = str(place_id).strip()
    save(s)


def remove(name):
    s = load()
    s.pop(name, None)
    save(s)


def parse_place_id(text):
    text = text.strip()
    m = re.search(r"/games/(\d+)", text)
    if m:
        return m.group(1)
    if text.isdigit():
        return text
    return None


def launch(place_id):
    url = f"roblox://experiences/start?placeId={place_id}"
    try:
        subprocess.Popen(["flatpak", "run", "org.vinegarhq.Sober", url],
                         env=sober.clean_env())
    except FileNotFoundError:
        pass
