# FPL-Team-Optimizer

FPL Site: https://fantasy.premierleague.com/
FPL Rules: https://fantasy.premierleague.com/help/rules

- Scrapes data from https://fplform.com/fpl-predicted-points
- Function uses PuLP to instantiate rules and set parameters/constraints as variables, linearly optimizes a team 
- Cleans scraped data, feeds into the function which outputs an optimized starting 11, bench of 4 players, captaincy selection, and points prediction.
