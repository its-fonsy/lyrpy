#!/usr/bin/python

import curses

class UI:

    def __init__(self):
        self.stdscr = curses.initscr()

        # getch() is blocking by default, with these func. just wait 150ms
        self.stdscr.nodelay(1)
        self.stdscr.timeout(150)
        curses.curs_set(0)


    def write_lyric(self, song_time, lyric):
        # Dimension of the terminal
        num_rows, num_cols = self.stdscr.getmaxyx()

        # Line that will be blank on top and bottom of the screen
        offset = 5
        info_lines = 2

        # Sometimes gives error if does just exit
        hl_verse, v = lyric.sync_verse(song_time)

        # Define the index of the verses that will be displayed
        # Highlight the center line
 
        if lyric.lenght() < (num_rows - offset):
            # If the lyrics can be contained in all the window then
            # adjust the offset to center all the text vertically
            offset = (num_rows - lyric.lenght()) // 2
            hl_line = v + offset
            render_start = 0
            render_end = lyric.lenght() - 1
        else:
            mid_line = num_rows // 2
            if v > (mid_line - offset):
                hl_line = mid_line
                render_start = v - mid_line + offset
                render_end = v + mid_line - offset

                if render_end > (lyric.lenght() - 1):
                    render_end = lyric.lenght() - 1

                    # Clear the lines when the lyrics can't cover all the screen
                    cl_line = num_rows- offset - ( render_end - v - 1 ) - mid_line
                    l = num_rows - offset
                    for i in range(cl_line):
                        self.stdscr.move(l, 0)
                        self.stdscr.clrtoeol()
                        l -= 1
            else:
                hl_line = v + offset
                render_start = 0
                render_end = num_rows - 2*offset

        # Print all the lyrics verses (no highlight)
        l = offset - info_lines
        for i in range(render_start, render_end):
            self.stdscr.move(l, 0)
            self.stdscr.clrtoeol()
            line = lyric.line(i)

            if len(line) > num_cols:
                self.stdscr.addstr(l, 2, line[:num_cols - 4])
            else:
                self.stdscr.addstr(l, num_cols//2 - len(line)//2, line)

            l += 1

        # Highlight the verse that is being singed
        self.stdscr.move(hl_line - info_lines, 0)
        self.stdscr.clrtoeol()
        line = lyric.line(v)
        self.stdscr.addstr(hl_line - info_lines, num_cols//2 - len(line)//2, line, curses.A_BOLD)

        # Clear the offset part of the screen to be sure that are blank line
        for i in range(offset - info_lines):
            self.stdscr.move(i, 0)
            self.stdscr.clrtoeol()

        for i in range(offset + info_lines):
            self.stdscr.move(num_rows - i - 1, 0)
            self.stdscr.clrtoeol()


    def write_no_lyrics_message(self):
        # Get tereminal dimension
        num_rows, num_cols = self.stdscr.getmaxyx()

        # Clear the screen
        for i in range(num_rows):
            self.stdscr.move(i, 0)
            self.stdscr.clrtoeol()

        message = "Lyrics not Found"
        self.stdscr.addstr(num_rows // 2 - 1 , num_cols//2 - len(message)//2, message, curses.A_BOLD)

        self.stdscr.refresh()


    def write_song_info(self, song_time, song_dur, lyric):
        # Get tereminal dimension
        num_rows, num_cols = self.stdscr.getmaxyx()

        # Getting minutes and second of the elapsed time of the song
        minute = 0
        elapsed = song_time
        duration = song_dur

        while (elapsed - 60.0) > 0.0:
            minute += 1
            elapsed = elapsed - 60.0

        elapsed = int(elapsed)
        if elapsed < 10.0:
            elapsed = '0' + str(elapsed)
        else:
            elapsed = str(elapsed)

        message = '[0' + str(minute) + ':' + elapsed + '/'

        # Getting minutes and second of the duration of the song
        minute = 0
        while (duration - 60.0) > 0.0:
            minute += 1
            duration = duration - 60.0

        duration = int(duration)

        if duration < 10.0:
            duration = '0' + str(duration)
        else:
            duration = str(duration)

        # time message is ready
        # ex: [01:37/05:03]
        message += '0' + str(minute) + ':' + duration + ']'
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
