"""Test to demonstrate the new ghost AI with scatter/chase/frightened behavior"""
from pacman.entities.ghost import Ghost
from pacman.entities.player import Player
from pacman.levels.loader import Level
from pacman.systems.game_state import GameState
from pacman.systems.ghost_ai import update_ghosts, tick_modes


def test_ghost_scatter_moves_to_corner():
    """Test that ghost in scatter mode moves toward its assigned corner"""
    grid = [
        "###########",
        "#.........#",
        "#.........#",
        "###########",
    ]
    lvl = Level(id="test", width=11, height=4, tile_grid=grid, pellet_positions=[], ghost_spawn_points=[], player_spawn={"x": 1, "y": 1})
    player = Player(x=1, y=1)
    gs = GameState(level=lvl, player=player)
    
    # Ghost starts at center, scatter corner is top-right
    ghost = Ghost(id="test", x=5, y=2, scatter_corner=(9, 1))
    gs.ghosts.append(ghost)
    gs.ghost_cycle_mode = "scatter"
    
    initial_dist = abs(ghost.x - 9) + abs(ghost.y - 1)
    
    # Run for 30 ticks
    for _ in range(30):
        gs.tick()
        tick_modes(gs)
        update_ghosts(gs)
    
    final_dist = abs(ghost.x - 9) + abs(ghost.y - 1)
    
    # Ghost should have moved closer to corner
    assert final_dist < initial_dist, f"Ghost should move toward corner: {initial_dist} -> {final_dist}"
    print(f"✓ Scatter test passed: distance to corner reduced from {initial_dist} to {final_dist}")


def test_ghost_chase_pursues_player():
    """Test that ghost in chase mode moves toward player"""
    grid = [
        "###########",
        "#.........#",
        "#.........#",
        "###########",
    ]
    lvl = Level(id="test", width=11, height=4, tile_grid=grid, pellet_positions=[], ghost_spawn_points=[], player_spawn={"x": 1, "y": 1})
    player = Player(x=1, y=1)
    gs = GameState(level=lvl, player=player)
    
    # Ghost starts far from player
    ghost = Ghost(id="test", x=9, y=2, scatter_corner=(9, 1))
    gs.ghosts.append(ghost)
    gs.ghost_cycle_mode = "chase"
    
    initial_dist = abs(ghost.x - player.x) + abs(ghost.y - player.y)
    
    # Run for 30 ticks
    for _ in range(30):
        gs.tick()
        tick_modes(gs)
        update_ghosts(gs)
    
    final_dist = abs(ghost.x - player.x) + abs(ghost.y - player.y)
    
    # Ghost should have moved closer to player
    assert final_dist < initial_dist, f"Ghost should chase player: {initial_dist} -> {final_dist}"
    print(f"✓ Chase test passed: distance to player reduced from {initial_dist} to {final_dist}")


def test_ghost_no_reversal():
    """Test that ghost doesn't immediately reverse direction"""
    grid = [
        "#########",
        "#.......#",
        "#########",
    ]
    lvl = Level(id="test", width=9, height=3, tile_grid=grid, pellet_positions=[], ghost_spawn_points=[], player_spawn={"x": 1, "y": 1})
    player = Player(x=1, y=1)
    gs = GameState(level=lvl, player=player)
    
    # Ghost moving right in a corridor
    ghost = Ghost(id="test", x=4, y=1, scatter_corner=(7, 1))
    ghost.dir_dx = 1  # moving right
    ghost.dir_dy = 0
    gs.ghosts.append(ghost)
    gs.ghost_cycle_mode = "scatter"
    
    # Run one movement cycle
    for _ in range(5):
        gs.tick()
        tick_modes(gs)
        update_ghosts(gs)
    
    # Ghost should not have reversed to move left (unless at intersection or blocked)
    # In a straight corridor, should continue right or stop, not reverse
    assert not (ghost.dir_dx == -1 and ghost.dir_dy == 0), "Ghost should not immediately reverse in corridor"
    print(f"✓ No-reversal test passed: ghost maintained forward motion")


def test_ghost_intersection_reconsideration():
    """Test that ghost reconsiders direction at intersections"""
    grid = [
        "#######",
        "#.....#",
        "#..#..#",
        "#.....#",
        "#######",
    ]
    lvl = Level(id="test", width=7, height=5, tile_grid=grid, pellet_positions=[], ghost_spawn_points=[], player_spawn={"x": 1, "y": 1})
    player = Player(x=1, y=1)
    gs = GameState(level=lvl, player=player)
    
    # Ghost at (2,2) - center of cross, has 4 directions available (true intersection)
    ghost = Ghost(id="test", x=2, y=2, scatter_corner=(5, 1))
    gs.ghosts.append(ghost)
    gs.ghost_cycle_mode = "scatter"
    
    # Ghost should be at an intersection (4 directions available)
    assert ghost.is_at_intersection(lvl), "Position (2,2) should be an intersection"
    
    # Run a few ticks
    for _ in range(10):
        gs.tick()
        tick_modes(gs)
        update_ghosts(gs)
    
    # Ghost should have moved (direction chosen at intersection)
    assert (ghost.x, ghost.y) != (2, 2), "Ghost should have moved from intersection"
    print(f"✓ Intersection test passed: ghost moved to ({ghost.x}, {ghost.y})")


if __name__ == "__main__":
    test_ghost_scatter_moves_to_corner()
    test_ghost_chase_pursues_player()
    test_ghost_no_reversal()
    test_ghost_intersection_reconsideration()
    print("\n✅ All ghost AI tests passed!")
