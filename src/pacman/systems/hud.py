def draw_hud_stub(score: int, lives: int) -> None:
    # Placeholder: integrate pygame rendering later
    _ = (score, lives)
    return


def ghost_modes_overlay(gs) -> list[tuple[str, str]]:
    """Return list of (ghost_id, mode) for debug overlay if enabled.

    T089: Optional debug HUD ghost mode overlay toggle.
    The GameState may expose `debug_show_ghost_modes`; if absent or False, returns empty list.
    """
    if not getattr(gs, "debug_show_ghost_modes", False):
        return []
    out: list[tuple[str, str]] = []
    cycle_mode = gs.ghost_cycle_mode
    for g in gs.ghosts:
        # Frightened overrides cycle display
        mode = "frightened" if gs.frightened_ticks_remaining > 0 else cycle_mode
        out.append((g.id, mode))
    return out
