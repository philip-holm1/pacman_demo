# QA Playtest Checklist

## Session Setup
- [ ] Confirm dependencies installed
- [ ] Run `python -m pacman` launches window
- [ ] Verify FPS overlay displays values

## Core Gameplay
- [ ] Player continuous movement works
- [ ] Ghosts move and respect walls
- [ ] Pellets consumed increment score
- [ ] Game over triggers at 0 lives
- [ ] Victory triggers when all pellets collected

## Powerups
- [ ] SpeedBoost increases movement speed
- [ ] GhostFreeze stops ghost movement
- [ ] ScoreMultiplier stacks (x2,x4,x8) cap enforced
- [ ] InvincibilityBlink prevents life loss on collision
- [ ] Timers pause correctly when game paused

## Scoring & Feedback
- [ ] Floating score feedback displays
- [ ] High score updates after round end
- [ ] Blink visual toggles ~0.2s interval

## Restart & States
- [ ] R key restarts from victory screen
- [ ] R key restarts from game over screen
- [ ] Post-restart state resets pellets, lives, score

## Performance & Stability
- [ ] Maintain >=30 FPS average
- [ ] Worst frame time < 100ms during session
- [ ] 5-min smoke playtest yields no crashes

## Long-Run Stability
- [ ] 60-min stability script completes
- [ ] No memory explosion or performance degradation

## Documentation
- [ ] README movement speeds accurate
- [ ] Powerup rules match observed behavior

## Final
- [ ] All tests pass (`pytest -q`)
- [ ] Pre-commit hooks run and pass
