import time
from typing import Optional, Tuple
from . import config
from .levels.loader import load_level
from .entities.player import Player
from .entities.ghost import Ghost
from .systems.game_state import GameState


def assign_scatter_corner(ghost_index: int, level_width: int, level_height: int) -> Tuple[int, int]:
    """Assign scatter corner based on ghost index (classic Pac-Man style).
    Ghost 0: top-right, Ghost 1: top-left, Ghost 2: bottom-right, Ghost 3: bottom-left
    """
    corners = [
        (level_width - 2, 1),           # top-right
        (1, 1),                          # top-left
        (level_width - 2, level_height - 2),  # bottom-right
        (1, level_height - 2),           # bottom-left
    ]
    return corners[ghost_index % len(corners)]
from .systems.collision import attempt_player_move, consume_pellet_if_present, apply_ghost_collision
from .systems.input import InputHandler
from .systems.render import render as render_frame
from .systems.screens import evaluate_state, handle_restart
from .systems.powerup_manager import powerup_manager
from .systems.scoring import apply_pellet_score, apply_powerup_bonus
from .systems.highscore import update_high_score, ensure_loaded
from .systems.hud_feedback import prune_feedback
from .systems.ghost_ai import update_ghosts, tick_modes
from .systems.perf import PerfTracker


def _spawn_initial_powerups(gs: GameState, count: int = 4) -> None:
    """Spawn initial powerups at game start for immediate availability.
    
    Removes some pellets to create empty floor tiles for powerup placement.
    
    Args:
        gs: GameState to spawn powerups in
        count: Number of powerups to spawn (default 4, one of each type)
    """
    powerup_types = ["SpeedBoost", "GhostFreeze", "ScoreMultiplier", "InvincibilityBlink"]
    
    # Remove some pellets scattered across the map to make room for powerups
    # Use deterministic selection: pick pellets at even intervals across the list
    total_pellets = len(gs.level.pellet_positions)
    if total_pellets > count * 10:  # Ensure we have enough pellets to space them out
        pellets_to_remove = []
        step = total_pellets // (count + 1)
        for i in range(count):
            idx = (i + 1) * step
            if idx < total_pellets:
                pellets_to_remove.append(idx)
        # Remove in reverse order to avoid index shifting
        for idx in reversed(pellets_to_remove):
            gs.level.pellet_positions.pop(idx)
    
    # Now spawn powerups in the cleared spaces
    spawned = 0
    for powerup_type in powerup_types[:count]:
        result = powerup_manager.spawn_powerup(gs, powerup_type=powerup_type)
        if result:
            spawned += 1
    if spawned > 0:
        print(f"[init] Spawned {spawned} initial powerups on map")


def run_placeholder(ticks: int = 5) -> None:
    """Run a minimal placeholder loop printing tick count then exit."""
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    # Load skin preference
    selected_skin = config.load_skin_preference()
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json", selected_skin=selected_skin)
    # Spawn ghosts from level definition with scatter corners
    for i, sp in enumerate(level.ghost_spawn_points):
        corner = assign_scatter_corner(i, level.width, level.height)
        gs.ghosts.append(Ghost(id=f"g{i+1}", x=sp.get("x", 0), y=sp.get("y", 0), scatter_corner=corner))
    ensure_loaded(gs)
    # Spawn initial powerups on the map
    _spawn_initial_powerups(gs)
    for i in range(ticks):
        gs.tick()
        print(f"tick={i} pellets={len(gs.level.pellet_positions)} lives={gs.player.lives}")
        time.sleep(0.01)


class FixedTimestepLoop:
    def __init__(self, state: GameState, target_fps: int = config.TICKS_PER_SECOND, input_handler: InputHandler | None = None, perf: PerfTracker | None = None) -> None:
        self.state = state
        self.target_fps = target_fps
        self.seconds_per_tick = 1.0 / target_fps
        self.running = True
        self.input = input_handler
        self.perf = perf

    def start(self, max_ticks: Optional[int] = None) -> None:
        self.running = True
        last = time.perf_counter()
        accumulator = 0.0
        while self.running:
            now = time.perf_counter()
            frame = now - last
            last = now
            accumulator += frame
            while accumulator >= self.seconds_per_tick:
                self.tick_logic()
                accumulator -= self.seconds_per_tick
                if max_ticks is not None and self.state.tick_count >= max_ticks:
                    self.running = False
                    break

    def tick_logic(self) -> None:
        tick_start = time.perf_counter()
        # Input first (toggle pause, movement intent)
        dx, dy = 0, 0
        if self.input is not None:
            sample = self.input.poll()
            if sample.quit_requested:
                self.running = False
                return
            if sample.pause_toggle:
                self.state.toggle_pause()
            if sample.restart and self.state.mode in ("victory", "game_over"):
                handle_restart(self.state)
            if sample.skin_toggle:
                # Cycle through available skins
                skin_names = list(config.AVAILABLE_SKINS.keys())
                current_idx = skin_names.index(self.state.selected_skin) if self.state.selected_skin in skin_names else 0
                next_idx = (current_idx + 1) % len(skin_names)
                self.state.selected_skin = skin_names[next_idx]
                config.save_skin_preference(self.state.selected_skin)
                # Clear sprite cache to force reload
                from .systems.render import _skin_sprite_cache
                _skin_sprite_cache.clear()
                print(f"[input] Skin changed to: {config.AVAILABLE_SKINS[self.state.selected_skin]['display_name']}")
            dx, dy = sample.move_dx, sample.move_dy
            # Update player's last movement direction if input present
            if (dx, dy) != (0, 0):
                self.state.player.last_move_dx = dx
                self.state.player.last_move_dy = dy

        self.state.tick()
        # Advance ghost FSM timers (even when player input absent)
        tick_modes(self.state)
        # Block all interactive updates except restart when not in playing mode
        if self.state.mode != "playing":
            # still allow high score update once when entering game over/victory
            if self.state.mode in ("victory", "game_over"):
                update_high_score(self.state)
            return

        if not self.state.paused:
            moved = False
            # Determine effective movement interval based on speed multiplier
            speed_mult = max(0.01, self.state.player.speed_multiplier)
            interval = max(1, int(config.BASE_PLAYER_MOVE_INTERVAL_TICKS / speed_mult))
            should_step = (self.state.tick_count % interval) == 0
            intended_dx, intended_dy = dx, dy
            if intended_dx == 0 and intended_dy == 0:
                # Preserve last movement if no new input
                intended_dx = self.state.player.last_move_dx
                intended_dy = self.state.player.last_move_dy
            if should_step and (intended_dx or intended_dy):
                moved = attempt_player_move(self.state.player, self.state.level, intended_dx, intended_dy)
                if moved:
                    # keep last direction consistent
                    self.state.player.last_move_dx = intended_dx
                    self.state.player.last_move_dy = intended_dy
            if not moved and self.input is None and should_step:
                # Fallback automated movement if no input handler
                moved = attempt_player_move(self.state.player, self.state.level, 1, 0)
                if not moved:
                    attempt_player_move(self.state.player, self.state.level, 0, 1)
            pellet_consumed = consume_pellet_if_present(self.state.player, self.state.level, self.state)
            # Check for powerup collection independently from pellets
            powerup_collected = powerup_manager.collect_powerup(self.state)
            apply_ghost_collision(self.state.player, self.state.ghosts)
            if pellet_consumed:
                apply_pellet_score(self.state)
                update_high_score(self.state)
            if powerup_collected:
                apply_powerup_bonus(self.state)
            powerup_manager.update_powerups(self.state)
            update_ghosts(self.state)
            evaluate_state(self.state)
            prune_feedback(self.state)
        if self.state.tick_count % config.TICKS_PER_SECOND == 0:
            print(f"[loop] seconds={self.state.tick_count // config.TICKS_PER_SECOND} pellets={len(self.state.level.pellet_positions)}")
        if self.perf is not None:
            self.perf.record_tick(time.perf_counter() - tick_start)


def run_interactive(max_ticks: int | None = None) -> None:
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    # Load skin preference
    selected_skin = config.load_skin_preference()
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json", selected_skin=selected_skin)
    for i, sp in enumerate(level.ghost_spawn_points):
        corner = assign_scatter_corner(i, level.width, level.height)
        gs.ghosts.append(Ghost(id=f"g{i+1}", x=sp.get("x", 0), y=sp.get("y", 0), scatter_corner=corner))
    ensure_loaded(gs)
    # Spawn initial powerups on the map
    _spawn_initial_powerups(gs)
    ih = InputHandler()
    screen = None
    if ih.available:
        screen = ih.init_window(width=level.width * 32, height=level.height * 32)
        try:
            perf = PerfTracker()
            loop = FixedTimestepLoop(gs, input_handler=ih, perf=perf)
            # Main loop with simple render each tick
            import pygame  # type: ignore
            target_fps = config.TICKS_PER_SECOND
            seconds_per_tick = 1.0 / target_fps
            last = time.perf_counter()
            accumulator = 0.0
            running = True
            while running and (max_ticks is None or gs.tick_count < max_ticks):
                now = time.perf_counter()
                frame = now - last
                last = now
                perf.record_frame(frame)
                accumulator += frame
                while accumulator >= seconds_per_tick:
                    loop.tick_logic()
                    accumulator -= seconds_per_tick
                if screen is not None:
                    render_frame(gs, screen, pygame, perf=perf)
                    pygame.display.flip()
                if not loop.running:
                    running = False
        finally:
            ih.shutdown()
    else:
        # Fallback to non-interactive placeholder if pygame unavailable
        run_placeholder(ticks=max_ticks or 5)
