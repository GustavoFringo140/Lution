import shutil
from pathlib import Path

SOBER_DATA = Path.home() / ".var/app/org.vinegarhq.Sober"

CLEANABLE = {
    "App Cache":    SOBER_DATA / "cache",
    "Shader Cache": SOBER_DATA / "data/sober/shaderCache",
    "Roblox Logs":  SOBER_DATA / "data/sober/logs",
}


def _dir_size_mb(path):
    if not path.exists():
        return 0.0
    total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    return round(total / (1024 * 1024), 2)


def scan():
    return {name: _dir_size_mb(p) for name, p in CLEANABLE.items()}


def clear(name):
    path = CLEANABLE.get(name)
    if not path or not path.exists():
        return 0.0
    freed = _dir_size_mb(path)
    shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True, exist_ok=True)
    return freed


def clear_all():
    return sum(clear(name) for name in CLEANABLE)
