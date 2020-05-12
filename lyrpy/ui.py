#!/usr/bin/python

import curses
from .lyric import sync_verse

def print_lyric(client, song_lyric, stdscr):
    # Dimension of the terminal
    num_rows, num_cols = stdscr.getmaxyx()

    # Line that will be blank on top and bottom of the screen
    offset = 5
    info_lines = 2

    # Sometimes gives error if does just exit
    playing_song_time = float(client.status()['elapsed'])
    hl_verse, v = sync_verse(playing_song_time, song_lyric)

    # Define the index of the verses that will be displayed
    # Highlight the center line
    if len(song_lyric) < (num_rows - offset):
        # If the lyrics can be contained in all the window then
        # adjust the offset to center all the text vertically
        offset = (num_rows - len(song_lyric)) // 2
        hl_line = v + offset
        render_start = 0
        render_end = len(song_lyric) - 1
    else:
        mid_line = num_rows // 2
        if v > (mid_line - offset):
            hl_line = mid_line
            render_start = v - mid_line + offset
            render_end = v + mid_line - offset

            if render_end > (len(song_lyric) - 1):
                render_end = len(song_lyric) - 1

                # Clear the lines when the lyrics can't cover all the screen
                cl_line = num_rows- offset - ( render_end - v - 1 ) - mid_line
                l = num_rows - offset
                for i in range(cl_line):
                    stdscr.move(l, 0)
                    stdscr.clrtoeol()
                    l -= 1
        else:
            hl_line = v + offset
            render_start = 0
            render_end = num_rows - 2*offset

    # OLD LAST LINE ON SCREEN SCROLL
    # if v > (num_rows - 2*offset):
    #     hl_line = num_rows - offset - 1
    #     render_start = v - (num_rows - 2*offset) + 1
    #     render_end = v
    # elif v == (num_rows - 2*offset):
    #     hl_line = num_rows - offset - 1
    #     render_start = 1
    #     render_end = num_rows - 2*offset + 1
    # else:
    #     hl_line = v + offset
    #     render_start = 0
    #     if len(lyric) < num_rows:
    #         render_end = len(lyric) - 1
    #     else:
    #         render_end = num_rows - 2*offset

    # Print all the lyrics verses (no highlight)
    l = offset - info_lines
    for i in range(render_start, render_end):
        stdscr.move(l, 0)
        stdscr.clrtoeol()
        line = str(song_lyric[i].get_verse())
        stdscr.addstr(l, num_cols//2 - len(line)//2, line)
        l += 1

    # Highlight the verse that is being singed
    stdscr.move(hl_line - info_lines, 0)
    stdscr.clrtoeol()
    line = str(song_lyric[v].get_verse())
    stdscr.addstr(hl_line - info_lines, num_cols//2 - len(line)//2, line, curses.A_BOLD)

    # Clear the offset part of the screen to be sure that are blank line
    for i in range(offset - info_lines):
        stdscr.move(i, 0)
        stdscr.clrtoeol()

    for i in range(offset + info_lines):
        stdscr.move(num_rows - i, 0)
        stdscr.clrtoeol()


def print_no_lyrics_message(stdscr):
    # Get tereminal dimension
    num_rows, num_cols = stdscr.getmaxyx()

    # Clear the screen
    for i in range(num_rows):
        stdscr.move(i, 0)
        stdscr.clrtoeol()

    message = "Lyrics not Found"
    stdscr.addstr(num_rows // 2 - 1 , num_cols//2 - len(message)//2, message, curses.A_BOLD)


def generating_lyrics_message(stdscr):
    # Get tereminal dimension
    num_rows, num_cols = stdscr.getmaxyx()

    # Clear the screen
    for i in range(num_rows):
        stdscr.move(i, 0)
        stdscr.clrtoeol()

    message = "Lyrics file found!"
    stdscr.addstr(num_rows // 2 - 1 , num_cols//2 - len(message)//2, message)

def print_song_info(stdscr, client):
    # Get tereminal dimension
    num_rows, num_cols = stdscr.getmaxyx()

    # Getting minutes and second of the elapsed time of the song
    minute = 0
    elapsed = float(client.status()['elapsed'])

    while (elapsed - 60.0) > 0.0:
        minute += 1
        elapsed = elapsed - 60.0

    elapsed = int(elapsed)
    if elapsed < 10.0:
        elapsed = '0' + str(elapsed)
    else:
        elapsed = str(elapsed)

    message = '0' + str(minute) + ':' + elapsed + '/'
    stdscr.addstr(num_rows - 3, 2, message )

    minute = 0
    duration = float(client.status()['duration'])

    # Getting minutes and second of the duration of the song
    while (duration - 60.0) > 0.0:
        minute += 1
        duration = duration - 60.0

    duration = int(duration)

    if duration < 10.0:
        duration = '0' + str(duration)
    else:
        duration = str(duration)

    message = '0' + str(minute) + ':' + duration
    stdscr.addstr(num_rows - 3, 8, message )

    # Print the artist and the title of the song
    title = client.currentsong()['title']
    artist = client.currentsong()['artist']
    message = artist + ' - ' + title
    stdscr.addstr(num_rows - 2, 2, message )

