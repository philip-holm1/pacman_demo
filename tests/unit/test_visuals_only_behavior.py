"""Test that skins are purely visual and don't affect gameplay mechanics."""
from pacman.systems.game_state import GameState
from pacman.levels.loader import Level, load_level
from pacman.entities.player import Player
from pacman.entities.ghost import Ghost
from pacman.systems.collision import attempt_player_move, consume_pellet_if_present


def test_collision_detection_unchanged_with_skin():
    """Test that collision detection works identically regardless of skin."""
    # Create two identical game states with different skins
    level = load_level("levels/level1.json")
    
    player1 = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    gs1 = GameState(level=level, player=player1, selected_skin="default")
    
    level2 = load_level("levels/level1.json")
    player2 = Player(x=level2.player_spawn["x"], y=level2.player_spawn["y"])
    gs2 = GameState(level=level2, player=player2, selected_skin="green_star")
    
    # Test wall collision
    # Try to move into a wall
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        moved1 = attempt_player_move(gs1.player, gs1.level, dx, dy)
        moved2 = attempt_player_move(gs2.player, gs2.level, dx, dy)
        assert moved1 == moved2, f"Movement result should be identical for direction ({dx}, {dy})"
    
    # Verify positions are still identical
    assert gs1.player.x == gs2.player.x
    assert gs1.player.y == gs2.player.y


def test_pellet_consumption_unchanged_with_skin():
    """Test that pellet consumption works identically regardless of skin."""
    level1 = load_level("levels/level1.json")
    player1 = Player(x=level1.player_spawn["x"], y=level1.player_spawn["y"])
    gs1 = GameState(level=level1, player=player1, selected_skin="default")
    
    level2 = load_level("levels/level1.json")
    player2 = Player(x=level2.player_spawn["x"], y=level2.player_spawn["y"])
    gs2 = GameState(level=level2, player=player2, selected_skin="green_star")
    
    # Get initial pellet count
    initial_pellets1 = len(gs1.level.pellet_positions)
    initial_pellets2 = len(gs2.level.pellet_positions)
    assert initial_pellets1 == initial_pellets2
    
    # Move to a pellet position and consume
    # Try to find a pellet near spawn
    if gs1.level.pellet_positions:
        pellet_pos = gs1.level.pellet_positions[0]
        gs1.player.x = pellet_pos["x"]
        gs1.player.y = pellet_pos["y"]
        gs2.player.x = pellet_pos["x"]
        gs2.player.y = pellet_pos["y"]
        
        consumed1 = consume_pellet_if_present(gs1.player, gs1.level, gs1)
        consumed2 = consume_pellet_if_present(gs2.player, gs2.level, gs2)
        
        assert consumed1 == consumed2, "Pellet consumption should be identical"
        assert len(gs1.level.pellet_positions) == len(gs2.level.pellet_positions), "Remaining pellets should be identical"


def test_game_state_attributes_independent_of_skin():
    """Test that GameState attributes work correctly with different skins."""
    level1 = load_level("levels/level1.json")
    player1 = Player(x=1, y=1, lives=3, score=100)
    gs1 = GameState(level=level1, player=player1, selected_skin="default")
    
    level2 = load_level("levels/level1.json")
    player2 = Player(x=1, y=1, lives=3, score=100)
    gs2 = GameState(level=level2, player=player2, selected_skin="green_star")
    
    # Test that game state attributes are independent
    assert gs1.selected_skin == "default"
    assert gs2.selected_skin == "green_star"
    
    # Test that changing skin doesn't affect other attributes
    gs1.selected_skin = "green_star"
    assert gs1.player.lives == 3
    assert gs1.player.score == 100
    assert gs1.mode == "playing"
    assert gs1.tick_count == 0


def test_timing_unchanged_with_skin():
    """Test that tick timing is not affected by skin selection."""
    level1 = load_level("levels/level1.json")
    player1 = Player(x=level1.player_spawn["x"], y=level1.player_spawn["y"])
    gs1 = GameState(level=level1, player=player1, selected_skin="default")
    
    level2 = load_level("levels/level1.json")
    player2 = Player(x=level2.player_spawn["x"], y=level2.player_spawn["y"])
    gs2 = GameState(level=level2, player=player2, selected_skin="green_star")
    
    # Advance both game states
    for _ in range(10):
        gs1.tick()
        gs2.tick()
    
    # Tick counts should be identical
    assert gs1.tick_count == gs2.tick_count == 10
    assert gs1.paused == gs2.paused == False
