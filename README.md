# FPL-Team-Optimizer

FPL Site: https://fantasy.premierleague.com/
FPL Rules: https://fantasy.premierleague.com/help/rules

- Scrapes data from https://fplform.com/fpl-predicted-points
- Function uses PuLP to instantiate rules and set parameters/constraints as variables, linearly optimizes a team 
- Cleans scraped data, feeds into the function which outputs an optimized starting 11, bench of 4 players, captaincy selection, and points prediction.

Run FPL-Team-Optimizer/fpl_bot/main. Change parameters in main as well, to adjust likelihood of bench being used, period oftime to optimize over, etc. Demonstration given in FPL Team Optimizer.ipynb
