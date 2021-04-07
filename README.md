# CheddarShredder
_the best opening is horse_

## Content
1. Introduction
2. Installation
3. Config

## Introduction
CheddarShredder is a python based iterative alpha beta search based chess engine. It can run in a terminal or in any UCI compatible chess GUI.

## Functions
- Works in terminal and UCI compatible chess GUIs
- Varies strength based on time left
- sometimes wins

## Installation
1. Clone this repository to your local hard drive.
2. Make sure Python 3 is installed. You can check by typing `python3 --version` into your terminal. If a string containing a version number is displayed, continue. Otherwise, install Python 3 from the [OFFICIAL WEBSITE](https://www.python.org/downloads).
3. Create a virtual python environment by typing `python3 -m venv <target folder>` into your terminal and switch to it using `source <target folder>/bin/activate`.
4. Install the required packages by running `python3 -m pip install -r requirements.txt` while the virtual environment is active.
5. To launch the terminal version of CheddarShredder, use the command `python3 main.py`.
6. If you want to use the engine in a UCI compatible chess GUI, select UCI.py as the engine.

## Roadmap
- [ ] Fix UCI

The current UCI support is a quickly hacked together mess. It currently supports a bare minimum of commands to work with lichess and doesn't give any live analysis updates. This should be fixed as soon as possible.
- [ ] Improve search algorithm

The current search algorithm uses move ordering to speed up alpha beta pruning but could be vastly improved by using hash tables for already computed evaluations. The evaluation function itself is also in a very early state, only considering material counts and basic piece positioning. Things like pawn structures, traps and endgame scenarios should definitely be included at some point.
