from src.pacman.levels.loader import load_level

def test_level_loader_basic():
    level = load_level("levels/level1.json")
    assert level.width == 10
    assert level.height == 10
    assert len(level.pellet_positions) == 3
    # Walls boundary check
    assert level.is_wall(0, 0)
    assert not level.is_wall(1, 1)
