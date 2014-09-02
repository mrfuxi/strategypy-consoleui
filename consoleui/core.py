import curses


class Game(object):

    PLAYER_COLORS = (
        curses.COLOR_GREEN,
        curses.COLOR_RED,
        curses.COLOR_YELLOW,
        curses.COLOR_CYAN,
    )

    def __init__(self, data, fps=30):
        self.data = data
        self.grid_size = data["grid_size"]
        self.frames = data["frames"]
        self.players = self.data["all_players"]
        self.winner = str(self.data["winner"])

        self.win = None
        self.info_win = None
        self.frame_sleep = 1000/fps

        self._setup_cursors()
        self._assign_colors_to_players()

    def _setup_cursors(self):
        curses.initscr()
        curses.curs_set(0)
        curses.start_color()

        self.win = curses.newwin(*self._win_size())
        info_size = self._info_win_size()
        self.info_win = curses.newwin(
            info_size[0],  # nlines
            info_size[1],  # ncols
            self._info_position(),  # y
            0  # x
        )

    def _win_size(self, border=True):
        """
        Return size of board
        """

        nlines, ncols = self.grid_size

        if border:
            nlines += 2
            ncols += 2

        return [nlines, ncols]

    def _info_win_size(self, border=True):
        """
        Return size of the info window
        """

        _, ncols = self.grid_size

        nlines = len(self.players)

        if border:
            nlines += 2
            ncols += 2

        return [nlines, ncols]

    def _info_position(self):
        """
        Return row location of the info window
        """

        nlines, _ = self._win_size()

        return nlines

    def _assign_colors_to_players(self):
        for i, player in enumerate(self.players):
            player_id = i + 1
            color = self.PLAYER_COLORS[i]
            curses.init_pair(player_id, color, curses.COLOR_BLACK)
            self.players[player]["color"] = curses.color_pair(player_id)

    def _player_color(self, player):
        return self.players[player]["color"]

    def _player_name(self, player):
        return self.players[player]["name"]

    def _print_frame(self, frame):
        self.win.erase()
        self.win.border()
        self.info_win.erase()
        self.info_win.border()

        for i, (player, state) in enumerate(frame.iteritems()):
            name = self._player_name(player)
            color = self._player_color(player)
            self.info_win.addstr(i + 1, 1, name, color)
            for bot, possition in state.iteritems():
                x, y = possition[0] + 1, possition[1] + 1
                self.win.addstr(x, y, player, color)

        self.win.refresh()
        self.info_win.refresh()
        curses.napms(self.frame_sleep)

    def _print_win_msg(self, wait=2000):
        self.info_win.erase()
        self.info_win.border()
        winner_name = self._player_name(self.winner)
        color = self._player_color(self.winner)
        self.info_win.addstr(1, 1, "Winner: %s" % winner_name, color)
        self.info_win.refresh()
        curses.napms(wait)

    def play(self):
        for frame in self.frames:
            self._print_frame(frame)

        self._print_win_msg()

        curses.endwin()
