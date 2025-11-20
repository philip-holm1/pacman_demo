from .game_state import GameState
from .. import config

def active_powerup_display(gs: GameState):
    items = []
    for inst in gs.player.active_powerups:
        remaining_ticks = inst.expires_at_tick - gs.tick_count
        remaining_sec = remaining_ticks / config.TICKS_PER_SECOND
        items.append({
            "type": inst.type,
            "remaining_seconds": round(remaining_sec, 2),
            "blink_on": gs.player.blink_on if inst.type == "InvincibilityBlink" else True,
        })
    return items

def render_powerup_hud_stub(gs: GameState):
    # Placeholder: return structured list for tests to assert timer freeze accuracy.
    return active_powerup_display(gs)
