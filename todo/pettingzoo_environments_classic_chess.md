Chess
../../../_images/classic_chess.gif
This environment is part of the classic environments. Please read that page first for general information.

Import

from pettingzoo.classic import chess_v6

Actions

Discrete

Parallel API

Yes

Manual Control

No

Agents

agents= ['player_0', 'player_1']

Agents

2

Action Shape

Discrete(4672)

Action Values

Discrete(4672)

Observation Shape

(8,8,111)

Observation Values

[0,1]

Chess is one of the oldest studied games in AI. Our implementation of the observation and action spaces for chess are what the AlphaZero method uses, with two small changes.

Observation Space
The observation is a dictionary which contains an 'observation' element which is the usual RL observation described below, and an 'action_mask' which holds the legal moves, described in the Legal Actions Mask section.

Like AlphaZero, the main observation space is an 8x8 image representing the board. It has 111 channels representing:

Channels 0 - 3: Castling rights:

Channel 0: All ones if white can castle queenside

Channel 1: All ones if white can castle kingside

Channel 2: All ones if black can castle queenside

Channel 3: All ones if black can castle kingside

Channel 4: Is black or white

Channel 5: A move clock counting up to the 50 move rule. Represented by a single channel where the n th element in the flattened channel is set if there has been n moves

Channel 6: All ones to help neural networks find board edges in padded convolutions

Channel 7 - 18: One channel for each piece type and player color combination. For example, there is a specific channel that represents black knights. An index of this channel is set to 1 if a black knight is in the corresponding spot on the game board, otherwise, it is set to 0. Similar to LeelaChessZero, en passant possibilities are represented by displaying the vulnerable pawn on the 8th row instead of the 5th.

Channel 19: represents whether a position has been seen before (whether a position is a 2-fold repetition)

Channel 20 - 111 represents the previous 7 boards, with each board represented by 13 channels. The latest board occupies the first 13 channels, followed by the second latest board, and so on. These 13 channels correspond to channels 7 - 20.

Similar to AlphaZero, our observation space follows a stacking approach, where it accumulates the previous 8 board observations.

Unlike AlphaZero, where the board orientation may vary, in our system, the env.board_history always maintains the orientation towards the white agent, with the white agent’s king consistently positioned on the 1st row. In simpler terms, both players are observing the same board layout.

Nevertheless, we have incorporated a convenient feature, the env.observe(‘player_1’) function, specifically for the black agent’s orientation. This facilitates the training of agents capable of playing proficiently as both black and white.

Legal Actions Mask
The legal moves available to the current agent are found in the action_mask element of the dictionary observation. The action_mask is a binary vector where each index of the vector represents whether the action is legal or not. The action_mask will be all zeros for any agent except the one whose turn it is. Taking an illegal move ends the game with a reward of -1 for the illegally moving agent and a reward of 0 for all other agents.

Action Space
From the AlphaZero chess paper:

[In AlphaChessZero, the] action space is a 8x8x73 dimensional array. Each of the 8×8 positions identifies the square from which to “pick up” a piece. The first 56 planes encode possible ‘queen moves’ for any piece: a number of squares [1..7] in which the piece will be moved, along one of eight relative compass directions {N, NE, E, SE, S, SW, W, NW}. The next 8 planes encode possible knight moves for that piece. The final 9 planes encode possible underpromotions for pawn moves or captures in two possible diagonals, to knight, bishop or rook respectively. Other pawn moves or captures from the seventh rank are promoted to a queen.

We instead flatten this into 8×8×73 = 4672 discrete action space.

You can get back the original (x,y,c) coordinates from the integer action a with the following expression: (a // (8*73), (a // 73) % 8, a % (8*73) % 73)

Example: >>> x = 6 >>> y = 0 >>> c = 12 >>> a = x*(873) + y73 + c >>> print(a // (873), a % (873) // 73, a % (8*73) % 73) 6 0 12

Note: the coordinates (6, 0, 12) correspond to column 6, row 0, plane 12. In chess notation, this would signify square G1:

0

1

2

3

4

5

6

7

A

B

C

D

E

F

G

H

Rewards
Winner

Loser

Draw

+1

-1

0

Version History
v6: Fixed wrong player starting first, check for insufficient material/50-turn rule/three fold repetition (1.23.2)

v5: Changed python-chess version to version 1.7 (1.13.1)

v4: Changed observation space to proper AlphaZero style frame stacking (1.11.0)

v3: Fixed bug in arbitrary calls to observe() (1.8.0)

v2: Legal action mask in observation replaced illegal move list in infos (1.5.0)

v1: Bumped version of all environments due to adoption of new agent iteration scheme where all agents are iterated over after they are done (1.4.0)

v0: Initial versions release (1.0.0)

Usage
AEC
from pettingzoo.classic import chess_v6

env = chess_v6.env(render_mode="human")
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        action = None
    else:
        mask = observation["action_mask"]
        # this is where you would insert your policy
        action = env.action_space(agent).sample(mask)

    env.step(action)
env.close()

API
class pettingzoo.classic.chess.chess.env(**kwargs)[source]
class pettingzoo.classic.chess.chess.raw_env(render_mode: str | None = None, screen_height: int | None = 800)[source]
action_space(agent)[source]
Takes in agent and returns the action space for that agent.

MUST return the same value for the same agent name

Default implementation is to return the action_spaces dict

close()[source]
Closes any resources that should be released.

Closes the rendering window, subprocesses, network connections, or any other resources that should be released.

observation_space(agent)[source]
Takes in agent and returns the observation space for that agent.

MUST return the same value for the same agent name

Default implementation is to return the observation_spaces dict

observe(agent)[source]
Returns the observation an agent currently can make.

last() calls this function.

render()[source]
Renders the environment as specified by self.render_mode.

Render mode can be human to display a window. Other render modes in the default environments are ‘rgb_array’ which returns a numpy array and is supported by all environments outside of classic, and ‘ansi’ which returns the strings printed (specific to classic environments).

reset(seed=None, options=None)[source]
Resets the environment to a starting state.

step(action)[source]
Accepts and executes the action of the current agent_selection in the environment.

Automatically switches control to the next agent.