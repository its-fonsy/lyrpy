#!/usr/bin/python

from . import ui
from . import lyric
from . import lyrics_folder # variable

import curses
import subprocess

from os import listdir
from os.path import isfile, join
from mpd import MPDClient


def loop(stdscr):
    # Connect to MPD server
    client = MPDClient()
    client.timeout = None
    client.idletimeout = None
    client.connect("localhost", 6600)

    # getch() is blocking by default, with these func. just wait 150ms
    stdscr.nodelay(1)
    stdscr.timeout(150)

    # Remove the cursor
    curses.curs_set(0)

    # Folder with all lyrics files
    lyrics_files = [f for f in listdir(lyrics_folder) if isfile(join(lyrics_folder, f))]

    artist = client.currentsong()['artist']
    title = client.currentsong()['title']
    prev_lyric = artist + ' - ' + title + '.lrc'
    if prev_lyric in lyrics_files:
        song_lyric = lyric.get_lyric_data(lyrics_folder + prev_lyric)
        song_lyric.sort()

    while (1):
        key = stdscr.getch()
        artist = client.currentsong()['artist']
        title = client.currentsong()['title']
        stdscr.clear()

        if(client.status()['state'] in ['play', 'pause']):
            # Checking if the lyrics is in the folder
            # Example of a file name: 'blink182 - First Date.lrc'
            lyric_filename = artist + ' - ' + title + '.lrc'

            if lyric_filename in lyrics_files:
                # Get the lyric if the song playing is new
                if prev_lyric != lyric_filename:
                    song_lyric = lyric.get_lyric_data(lyrics_folder + lyric_filename)

                    # Inform the user that the lyrics is found
                    ui.generating_lyrics_message(stdscr)
                    stdscr.box()
                    stdscr.refresh()
                    song_lyric.sort()
                    prev_lyric = lyric_filename

                # Print the lyric
                try:
                    ui.print_lyric(client, song_lyric, stdscr)
                except:
                    pass
                ui.print_song_info(stdscr, client)

            else:
                ui.print_no_lyrics_message(stdscr)
                ui.print_song_info(stdscr, client)

            # Draw the border of the window
            stdscr.box()
            stdscr.refresh()

        if ( key == ord('q') ):
            # Press 'q' to exit
            break

        if ( key == ord('?') ):
            ui.print_help_message(stdscr)

    client.close()
    client.disconnect()


def main():
    curses.wrapper(loop)


if __name__ == "__main__":
    main()
