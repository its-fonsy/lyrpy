#!/usr/bin/python

import curses
import subprocess
from os import listdir
from os.path import isfile, join

from gen_lyric import *
from mpd_fct import *


def print_lyric(client, lyric, stdscr):
    # Dimension of the terminal
    num_rows, num_cols = stdscr.getmaxyx()

    # Line that will be blank on top and bottom of the screen
    top_bot_offset = 5
    info_lines = 2

    # Sometimes gives error if does just exit
    playing_song_time = float(client.status()['elapsed'])
    hl_verse, v = sync_verse(playing_song_time, lyric)

    # Define the index of the verses that will be displayed
    # Highlight the center line
    if len(lyric) < (num_rows - top_bot_offset):
        # If the lyrics can be contained in all the window then
        # adjust the top_bot_offset to center all the text vertically
        top_bot_offset = (num_rows - len(lyric)) // 2
        hl_line = v + top_bot_offset
        render_start = 0
        render_end = len(lyric) - 1
    else:
        mid_line = num_rows // 2
        if v > (mid_line - top_bot_offset):
            hl_line = mid_line
            render_start = v - mid_line + top_bot_offset
            render_end = v + mid_line - top_bot_offset

            if render_end > (len(lyric) - 1):
                render_end = len(lyric) - 1

                # Clear the lines when the lyrics can't cover all the screen
                cl_line = num_rows- top_bot_offset - ( render_end - v - 1 ) - mid_line
                l = num_rows - top_bot_offset
                for i in range(cl_line):
                    stdscr.move(l, 0)
                    stdscr.clrtoeol()
                    l -= 1
        else:
            hl_line = v + top_bot_offset
            render_start = 0
            render_end = num_rows - 2*top_bot_offset

    # OLD LAST LINE ON SCREEN SCROLL
    # if v > (num_rows - 2*top_bot_offset):
    #     hl_line = num_rows - top_bot_offset - 1
    #     render_start = v - (num_rows - 2*top_bot_offset) + 1
    #     render_end = v
    # elif v == (num_rows - 2*top_bot_offset):
    #     hl_line = num_rows - top_bot_offset - 1
    #     render_start = 1
    #     render_end = num_rows - 2*top_bot_offset + 1
    # else:
    #     hl_line = v + top_bot_offset
    #     render_start = 0
    #     if len(lyric) < num_rows:
    #         render_end = len(lyric) - 1
    #     else:
    #         render_end = num_rows - 2*top_bot_offset

    # Print all the lyrics verses (no highlight)
    l = top_bot_offset - info_lines
    for i in range(render_start, render_end):
        stdscr.move(l, 0)
        stdscr.clrtoeol()
        line = str(lyric[i].get_verse())
        stdscr.addstr(l, num_cols//2 - len(line)//2, line)
        l += 1

    # Highlight the verse that is being singed
    stdscr.move(hl_line - info_lines, 0)
    stdscr.clrtoeol()
    line = str(lyric[v].get_verse())
    stdscr.addstr(hl_line - info_lines, num_cols//2 - len(line)//2, line, curses.A_BOLD)

    # Clear the top_bot_offset part of the screen to be sure that are blank line
    for i in range(top_bot_offset - info_lines):
        stdscr.move(i, 0)
        stdscr.clrtoeol()

        stdscr.move(num_rows - i - 1 - info_lines, 0)
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


def ui(stdscr):
    # Connect to MPD server
    client = connect_client()

    # getch() is blocking by default, with these func. just wait 150ms
    stdscr.nodelay(1)
    stdscr.timeout(150)

    # Remove the cursor
    curses.curs_set(0)

    # Folder with all lyrics files
    lyrics_folder = '/home/fonsy/musica/foobar/lyrics/'
    lyrics_files = [f for f in listdir(lyrics_folder) if isfile(join(lyrics_folder, f))]

    artist = client.currentsong()['artist']
    title = client.currentsong()['title']
    prev_lyric = artist + ' - ' + title + '.lrc'
    if prev_lyric in lyrics_files:
        lyric = get_lyric_data(lyrics_folder + prev_lyric)
        lyric.sort()

    while (1):
        key = stdscr.getch()

        artist = client.currentsong()['artist']
        title = client.currentsong()['title']

        if(client.status()['state'] == 'play'):

            # Checking if the lyrics is in the folder
            # Example of a file name: 'blink182 - First Date.lrc'
            lyric_filename = artist + ' - ' + title + '.lrc'

            if lyric_filename in lyrics_files:

                # Get the lyric if the song playing is new
                if prev_lyric != lyric_filename:
                    lyric = get_lyric_data(lyrics_folder + lyric_filename)

                    # Inform the user that the lyrics is found
                    generating_lyrics_message(stdscr)
                    stdscr.box()
                    stdscr.refresh()

                    lyric.sort()

                    prev_lyric = lyric_filename

                # Print the lyric
                try:
                    print_lyric(client, lyric, stdscr)
                except:
                    pass
                print_song_info(stdscr, client)

            else:
                print_no_lyrics_message(stdscr)
                print_song_info(stdscr, client)

            # Draw the border of the window
            stdscr.box()
            stdscr.refresh()

        if ( key == ord('q') ):
            # Press 'q' to exit
            break
        if ( key == ord('o') ):
            # Press 'o' to open the lyric file
            curses.endwin()
            subprocess.run(["nvim", lyrics_folder + lyric_filename])

            # Refresh the current lyric
            prev_lyric = "Change the lyric bro"


if __name__ == '__main__':
    curses.wrapper(ui)
