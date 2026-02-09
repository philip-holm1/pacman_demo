# quickstart.md — Run the Pacman Demo (local)

Prerequisites
- Python 3.10+ (3.11 recommended)
- pip

Quick start (development)

1. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install pygame pytest
```

2. Run the game (from repo root):

```powershell
python -m src.pacman
```

3. Run tests:

```powershell
python -m pytest tests/unit
```

Notes
- If display issues arise on headless CI, consider mocking or isolating `pygame` imports in pure-logic modules and test those directly.
- Game configuration (starting lives, tick rate) will live in `src/pacman/config.py` or `levels/level1.json`.

