# Connect-4-AI
### Command Line Interface

| Command | Description | Example | Default |
| --- | --- | --- | --- | 
| `-p1` | Agent who will be acting as player 1. | -p1 minimaxAI | human |
| `-p2` | Agent who will be acting as player 2. | -p2 monteCarloAI | human |
| `-seed` | Seed for AI’s with stochastic elements | -seed 0 | 0 |
| `-w` | Rows of gameboard. | -w 6 | 6 |
| `-l` | Columns of gameboard. | -l 7 | 7 |
| `-visualize` | Agent who will be acting as player 2. | -visualize True | True |
| `-verbose` | Sends move-by-move game history to shell | -verbose True | False |
| `-limit_players` | Which agents should have time limits. | -limit_players 1,2 | 1,2 |
| `-time_limit` | Time limit for each player. No effect if a player is not limited. In the format “x,y” where x and y are floating point numbers. | -time_limit 0.5,0.5 | 0.5,0.5 |

### Commands
#### To play against the AI use  `python main.py -p2 alphaBetaAI -limit_players 2 -visualize True -verbose True`
