import json
import sys
import curses

from core import Game

output = sys.stdin.read()
data = json.loads(output)

try:
    game = Game(data)
    game.play()
finally:
    curses.endwin()
