import time
from typing import Optional
from . import config
from .levels.loader import load_level
from .entities.player import Player
from .entities.ghost import Ghost
from .systems.game_state import GameState
from .systems.collision import attempt_player_move, consume_pellet_if_present, apply_ghost_collision
from .systems.input import InputHandler
from .systems.render import render as render_frame
from .systems.screens import evaluate_state, handle_restart
from .systems.powerup_manager import powerup_manager
from .systems.scoring import apply_pellet_score, apply_powerup_bonus
from .systems.highscore import update_high_score, ensure_loaded
from .systems.hud_feedback import prune_feedback
from .systems.ghost_ai import update_ghosts


def run_placeholder(ticks: int = 5) -> None:
    """Run a minimal placeholder loop printing tick count then exit."""
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")
    # Spawn ghosts from level definition
    for i, sp in enumerate(level.ghost_spawn_points):
        gs.ghosts.append(Ghost(id=f"g{i+1}", x=sp.get("x", 0), y=sp.get("y", 0)))
    ensure_loaded(gs)
    for i in range(ticks):
        gs.tick()
        print(f"tick={i} pellets={len(gs.level.pellet_positions)} lives={gs.player.lives}")
        time.sleep(0.01)


class FixedTimestepLoop:
    def __init__(self, state: GameState, target_fps: int = config.TICKS_PER_SECOND, input_handler: InputHandler | None = None) -> None:
        self.state = state
        self.target_fps = target_fps
        self.seconds_per_tick = 1.0 / target_fps
        self.running = True
        self.input = input_handler

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
            dx, dy = sample.move_dx, sample.move_dy
            # Update player's last movement direction if input present
            if (dx, dy) != (0, 0):
                self.state.player.last_move_dx = dx
                self.state.player.last_move_dy = dy

        self.state.tick()
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
            apply_ghost_collision(self.state.player, self.state.ghosts)
            if pellet_consumed:
                # attempt collect if powerup under player (manager uses level pellet list as placeholder store)
                powerup_manager.collect_powerup(self.state)
                apply_pellet_score(self.state)
                update_high_score(self.state)
            powerup_manager.update_powerups(self.state)
            # Ghost movement only in interactive loop (input handler present)
            if self.input is not None:
                update_ghosts(self.state)
            evaluate_state(self.state)
            prune_feedback(self.state)
            if self.state.mode in ("victory", "game_over"):
                update_high_score(self.state)
        if self.state.tick_count % config.TICKS_PER_SECOND == 0:
            print(f"[loop] seconds={self.state.tick_count // config.TICKS_PER_SECOND} pellets={len(self.state.level.pellet_positions)}")


def run_interactive(max_ticks: int | None = None) -> None:
    level = load_level("levels/level1.json")
    player = Player(x=level.player_spawn["x"], y=level.player_spawn["y"])
    gs = GameState(level=level, player=player, level_source_path="levels/level1.json")
    for i, sp in enumerate(level.ghost_spawn_points):
        gs.ghosts.append(Ghost(id=f"g{i+1}", x=sp.get("x", 0), y=sp.get("y", 0)))
    ensure_loaded(gs)
    ih = InputHandler()
    screen = None
    if ih.available:
        screen = ih.init_window(width=level.width * 32, height=level.height * 32)
        try:
            loop = FixedTimestepLoop(gs, input_handler=ih)
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
                accumulator += frame
                while accumulator >= seconds_per_tick:
                    loop.tick_logic()
                    accumulator -= seconds_per_tick
                if screen is not None:
                    render_frame(gs, screen, pygame)
                    pygame.display.flip()
                if not loop.running:
                    running = False
        finally:
            ih.shutdown()
    else:
        # Fallback to non-interactive placeholder if pygame unavailable
        run_placeholder(ticks=max_ticks or 5)
