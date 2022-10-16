#!/usr/bin/python

import curses

class UI:

    def __init__(self):
        self.stdscr = curses.initscr()

        # getch() is blocking by default, with these func. just wait 150ms
        self.stdscr.nodelay(1)
        self.stdscr.timeout(150)
        curses.curs_set(0)

        # Line that will be blank on top and bottom of the screen
        self.blank_lines = 3
        self.info_lines = 1

    def print_lyric(self, playing_time, lyric):

        num_rows, num_cols = self.stdscr.getmaxyx()
        l = lyric.lyric
        _, svi = lyric.singed_verse(playing_time)

        max_lines_to_print = num_rows - 2*self.blank_lines - self.info_lines

        # Print lyirc that are shorter then the number of TERM rows
        if ( len(l) < max_lines_to_print ):
            self.print_verses_from_to(l, 0, len(l)-1, svi)
            return

        # Print lyirc that are at the beginning of the song
        if( svi < max_lines_to_print//2 ):
            self.print_verses_from_to(l, 0, max_lines_to_print, svi)
            return

        # Print lyirc that are at the end of the song
        if ( svi > (len(l) - max_lines_to_print//2) ):
            self.print_verses_from_to(l,
                                   len(l) - max_lines_to_print,
                                   max_lines_to_print,
                                   svi)
            return

        # Print lyirc that are in the middle of the song
        self.print_verses_from_to(l,
                               svi - max_lines_to_print//2,
                               max_lines_to_print,
                               svi)


    def print_verses_from_to(self, l, start_idx, end_idx, svi):

        num_rows, num_cols = self.stdscr.getmaxyx()

        for i in range(end_idx):
            self.stdscr.move(self.blank_lines + i, 0)
            self.stdscr.clrtoeol()
            verse = l[i + start_idx].get_verse()

            y = self.blank_lines + i

            if len(verse) > (num_cols - 4):
                self.stdscr.addstr(y, 2, verse[:num_cols - 4],
                           curses.A_BOLD if svi == (i + start_idx) else 0)
            else:
                self.stdscr.addstr(y, num_cols//2 - len(verse)//2, verse,
                           curses.A_BOLD if svi == (i + start_idx) else 0)


    def print_no_lyrics_message(self):
        # Get tereminal dimension
        num_rows, num_cols = self.stdscr.getmaxyx()

        # Clear the screen
        for i in range(num_rows):
            self.stdscr.move(i, 0)
            self.stdscr.clrtoeol()

        message = "Lyrics not Found"
        self.stdscr.addstr(num_rows // 2 - 1,
                           num_cols//2 - len(message)//2,
                           message,
                           curses.A_BOLD)

        self.stdscr.refresh()


    def print_debug_message(self, message):
        # Get tereminal dimension
        num_rows, num_cols = self.stdscr.getmaxyx()

        # Clear the screen
        for i in range(num_rows):
            self.stdscr.move(i, 0)
            self.stdscr.clrtoeol()

        self.stdscr.addstr(num_rows // 2 - 1,
                           num_cols//2 - len(message)//2,
                           message,
                           curses.A_BOLD)

        self.stdscr.refresh()


    def get_min_sec(self, seconds):
        minutes = 0

        while (seconds - 60.0) > 0.0:
            minutes += 1
            seconds -= 60.0

        return minutes, int(seconds)


    def print_song_info(self, song_time, song_dur, lyric):
        # Get tereminal dimension
        num_rows, num_cols = self.stdscr.getmaxyx()

        # Getting minutes and second of the elapsed time of the song
        p_min, p_sec = self.get_min_sec(song_time)
        p_sec = '0' + str(p_sec) if p_sec < 10.00 else str(p_sec)
        message = '[0' + str(p_min) + ':' + p_sec + '/'

        # Getting minutes and second of the duration of the song
        max_min, max_sec = self.get_min_sec(song_dur)
        max_sec = '0' + str(max_sec) if max_sec < 10.00 else str(max_sec)

        # time message is ready
        # ex: [01:37/05:03]
        message += '0' + str(max_min) + ':' + max_sec + ']'
        self.stdscr.addstr(num_rows - 1, num_cols - 14, message, curses.A_BOLD)

        # Print the artist and the title of the song
        artist, title = lyric.get_info()
        message = artist + ' - ' + title
        self.stdscr.addstr(num_rows - 1, 2, 'Playing: ', curses.A_BOLD)
        self.stdscr.addstr(num_rows - 1, 11, message )

        self.stdscr.refresh()


    def key_pressed(self):
        return self.stdscr.getch()


    def kill(self):
        curses.endwin()
