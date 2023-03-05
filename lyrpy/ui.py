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
        self.blank_lines = 2
        self.info_lines = 1

    def print_lyric(self, playing_time, lyric):

        num_rows, num_cols = self.stdscr.getmaxyx()
        l = lyric.lyric
        lyric_len = len(l)
        _, svi = lyric.singed_verse(playing_time)

        max_lines_to_print = num_rows - 2*self.blank_lines - self.info_lines
        middle_row = max_lines_to_print//2

        # Helping debug indexes
        # self.stdscr.addstr(num_rows-2,0,f"max_lines_to_print={max_lines_to_print}"
        #                          f" row={num_rows}"
        #                          f" col={num_cols}"
        #                          f" svi={svi}"
        #                          f" middle_row={middle_row}"
        #                          )

        # Print lyirc that are shorter then the number of TERM rows
        if ( lyric_len < max_lines_to_print ):
            self.print_verses_from_to(l, 0, lyric_len - 1, svi)
            return

        # Print lyirc that are at the beginning of the song
        if( svi < middle_row ):
            self.print_verses_from_to(l, 0, max_lines_to_print, svi)
            return

        # Print lyirc that are at the end of the song
        if ( svi > (lyric_len - middle_row - self.blank_lines) ):
            self.print_verses_from_to(l,
                                   lyric_len - max_lines_to_print - 1,
                                   max_lines_to_print,
                                   svi)
            return

        # Print lyirc that are in the middle of the song
        self.print_verses_from_to(l,
                               svi - middle_row,
                               max_lines_to_print,
                               svi)


    def print_verses_from_to(self, l, start_idx, end_idx, svi):

        num_rows, num_cols = self.stdscr.getmaxyx()

        # Helping debug indexes
        # self.stdscr.addstr(num_rows-3,0,f"fpr={self.blank_lines}")

        for i in range(end_idx):
            y = self.blank_lines + i

            self.stdscr.move(y, 0)
            self.stdscr.clrtoeol()
            verse = l[i + start_idx].get_verse()

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

        message = "LYRIC NOT FOUND :("
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

        # clear the info lines
        self.stdscr.move(num_rows - 2, 0)
        self.stdscr.clrtoeol()
        self.stdscr.move(num_rows - 1, 0)
        self.stdscr.clrtoeol()

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

        artist, title = lyric.get_info()

        # Print the artist
        self.stdscr.addstr(num_rows - 2, 2, 'Artist: ', curses.A_BOLD)

        if( len(artist) > num_cols - 10 ):
            self.stdscr.addstr(num_rows - 2, 10, artist[0: num_cols - 10 - 4] + '... ' )
        else:
            self.stdscr.addstr(num_rows - 2, 10, artist)

        # Print the track
        self.stdscr.addstr(num_rows - 1, 2, ' Title: ', curses.A_BOLD)

        if( len(title) > num_cols - 24 ):
            self.stdscr.addstr(num_rows - 1, 10, title[0: num_cols - 24 - 4] + '... ' )
        else:
            self.stdscr.addstr(num_rows - 1, 10, title)

        self.stdscr.refresh()


    def key_pressed(self):
        return self.stdscr.getch()


    def kill(self):
        curses.endwin()
