TICKS_PER_SECOND = 60
DEFAULT_POWERUP_DURATION = 8.0
START_LIVES = 3
# Spec uses POWERUP_PELLET_INTERVAL terminology; retain old name for compatibility
POWERUP_PELLET_THRESHOLD = 30  # spawn attempt every N pellets consumed
POWERUP_PELLET_INTERVAL = POWERUP_PELLET_THRESHOLD
MAX_SCORE_MULTIPLIER = 8
BASE_PLAYER_MOVE_INTERVAL_TICKS = 8  # player moves every 8 ticks (~7.5 tiles/sec baseline)
GHOST_MOVE_INTERVAL_TICKS = 10  # ghosts move every 10 ticks (~6 tiles/sec - slower than player for escapeability)
GHOST_DECISION_INTERVAL_TICKS = 5  # deprecated - now decisions made at intersections
FRIGHTENED_EXTENSION_TICKS = 180  # 3 seconds
SCATTER_DURATION_TICKS = 420  # 7 seconds
CHASE_DURATION_TICKS = 1200  # 20 seconds
