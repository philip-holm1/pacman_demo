# pacman_demo Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-11-19

## Active Technologies
- Python 3.x (repo uses `python -m pacman`) + pygame (likely; NEEDS CLARIFICATION), json for config/persistence (001-skins-green-star)
- Local files (`data/highscore.json`, config in code or simple JSON) (001-skins-green-star)

- Python 3.11 (target; accept 3.10 where needed) + `pygame` (rendering/input/audio), `pytest` (tests), `pyyaml` or built-in `json` (level/config parsing). Optional dev tools: `black`, `ruff`. (master)

## Project Structure

```text
src/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Python 3.11 (target; accept 3.10 where needed): Follow standard conventions

## Recent Changes
- 001-skins-green-star: Added Python 3.x (repo uses `python -m pacman`) + pygame (likely; NEEDS CLARIFICATION), json for config/persistence

- master: Added Python 3.11 (target; accept 3.10 where needed) + `pygame` (rendering/input/audio), `pytest` (tests), `pyyaml` or built-in `json` (level/config parsing). Optional dev tools: `black`, `ruff`.

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
