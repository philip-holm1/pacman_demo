from .game_state import GameState
from .. import config
from typing import List, Tuple

def tick_modes(gs: GameState) -> None:
    """Advance ghost FSM timers every tick (independent of movement interval)."""
    if gs.mode != "playing" or gs.paused:
        return
    # Frightened overrides cycle
    if gs.frightened_ticks_remaining > 0:
        gs.frightened_ticks_remaining -= 1
        if gs.frightened_ticks_remaining <= 0:
            # restore underlying cycle state
            gs.ghost_cycle_mode = gs._underlying_cycle_mode
            gs.ghost_cycle_ticks = gs._underlying_cycle_ticks_snapshot
            # Force direction reconsideration on mode change
            for g in gs.ghosts:
                if g.state != "frozen":
                    g.dir_dx = 0
                    g.dir_dy = 0
        return
    gs.ghost_cycle_ticks += 1
    if gs.ghost_cycle_mode == "scatter" and gs.ghost_cycle_ticks >= config.SCATTER_DURATION_TICKS:
        gs.ghost_cycle_mode = "chase"
        gs.ghost_cycle_ticks = 0
        # Force direction reconsideration on mode change
        for g in gs.ghosts:
            if g.state != "frozen":
                g.dir_dx = 0
                g.dir_dy = 0
    elif gs.ghost_cycle_mode == "chase" and gs.ghost_cycle_ticks >= config.CHASE_DURATION_TICKS:
        gs.ghost_cycle_mode = "scatter"
        gs.ghost_cycle_ticks = 0
        # Force direction reconsideration on mode change
        for g in gs.ghosts:
            if g.state != "frozen":
                g.dir_dx = 0
                g.dir_dy = 0

def trigger_frightened(gs: GameState, extension_ticks: int | None = None) -> None:
    """Enter or extend frightened mode. Underlying cycle timers pause and resume deterministically."""
    if extension_ticks is None:
        extension_ticks = config.FRIGHTENED_EXTENSION_TICKS
    if gs.frightened_ticks_remaining > 0:
        gs.frightened_ticks_remaining += extension_ticks
    else:
        gs._underlying_cycle_mode = gs.ghost_cycle_mode
        gs._underlying_cycle_ticks_snapshot = gs.ghost_cycle_ticks
        gs.frightened_ticks_remaining = extension_ticks
        gs.ghost_cycle_mode = "frightened"

def update_ghosts(gs: GameState) -> None:
    """Advance ghost positions with intelligent AI based on current mode.
    
    Movement is throttled by GHOST_MOVE_INTERVAL_TICKS.
    Scatter: Move toward assigned corner.
    Chase: Move toward player position.
    Frightened: Random movement (seeded RNG).
    """
    if gs.paused or gs.mode != "playing":
        return
    # Note: tick_modes() is called in main game loop, not here
    if (gs.tick_count % config.GHOST_MOVE_INTERVAL_TICKS) != 0:
        return
    
    for g in gs.ghosts:
        if g.state == "frozen":
            continue
            
        if gs.ghost_cycle_mode == "frightened":
            # Frightened: random movement with no-reversal rule
            valid_dirs = g.get_valid_directions(gs.level)
            if not valid_dirs:
                continue
                
            # Apply no-reversal rule
            opposite = (-g.dir_dx, -g.dir_dy)
            if len(valid_dirs) > 1 and opposite in valid_dirs:
                valid_dirs = [d for d in valid_dirs if d != opposite]
            
            # Choose random direction at intersections
            if g.is_at_intersection(gs.level):
                choice = gs.frightened_rng.choice(valid_dirs)
                g.dir_dx, g.dir_dy = choice
            elif (g.dir_dx, g.dir_dy) not in valid_dirs:
                # Blocked, choose new direction
                choice = gs.frightened_rng.choice(valid_dirs)
                g.dir_dx, g.dir_dy = choice
            
            # Move
            nx = g.x + g.dir_dx
            ny = g.y + g.dir_dy
            if not gs.level.is_wall(nx, ny):
                g.x, g.y = nx, ny
                
        elif gs.ghost_cycle_mode == "scatter":
            # Scatter: move toward assigned corner
            g.step_toward_target(gs.level, g.scatter_corner[0], g.scatter_corner[1])
            
        elif gs.ghost_cycle_mode == "chase":
            # Chase: move toward player position
            g.step_toward_target(gs.level, gs.player.x, gs.player.y)
