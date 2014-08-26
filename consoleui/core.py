import curses


class Game(object):

    PLAYER_COLORS = (
        curses.COLOR_GREEN,
        curses.COLOR_RED,
        curses.COLOR_YELLOW,
        curses.COLOR_CYAN,
    )

    def __init__(self, data):
        self.data = data
        self.grid_size = data["grid_size"]
        self.frames = data["frames"]
        self.players = self.data["all_players"]

        curses.initscr()
        curses.curs_set(0)
        curses.start_color()
        for i, player in enumerate(self.players):
            player_id = i + 1
            color = self.PLAYER_COLORS[i]
            curses.init_pair(player_id, color, curses.COLOR_BLACK)
            self.players[player]["color"] = curses.color_pair(player_id)

        self.win = curses.newwin(
            self.grid_size[0] + 2,
            self.grid_size[0] + 2,
        )

    def _player_color(self, player):
        return self.players[player]["color"]

    def _print_frame(self, frame):
        curses.napms(150)
        self.win.erase()
        self.win.border()

        for player, state in frame.iteritems():
            color = self._player_color(player)
            for bot, possition in state.iteritems():
                x, y = possition[0] + 1, possition[1] + 1
                self.win.addstr(x, y, player, color)
        self.win.refresh()

    def play(self):
        for frame in self.frames:
            self._print_frame(frame)

        curses.endwin()
