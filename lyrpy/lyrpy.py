#!/usr/bin/python

from . import ui
from . import lyric
from . import config

import argparse
import curses
import subprocess

from os import listdir
from os.path import isfile, join
from mpd import MPDClient

# Read the config file in $HOME/.config/lyrpy
lyr_config = config.read()
lyrics_folder = lyr_config['Default']['lyrics_directory']
editor = lyr_config['Default']['editor']

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

        if(client.status()['state'] == 'play'):

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
        if ( key == ord('o') ):
            # Press 'o' to open the lyric file
            curses.endwin()
            subprocess.run([editor, lyrics_folder + lyric_filename])

            # Refresh the current lyric
            prev_lyric = "Change the lyric bro"
            lyrics_files = [f for f in listdir(lyrics_folder) if isfile(join(lyrics_folder, f))]

    client.close()
    client.disconnect()


def main():
    parser = argparse.ArgumentParser( \
                description='Display sync lyric of the current playing song on mpd server')

    parser.add_argument('-d', '--lyrics-dir', nargs=1, \
                         help="Specify the location of the lyrics directory")
    parser.add_argument('-e', '--editor', nargs=1 , \
                         help="Specify the editor to use to modify lyrics file")

    # Args overwrite the config file
    args = parser.parse_args()
    if args.lyrics_dir:
        global lyrics_folder
        lyrics_folder = args.lyrics_folder[0]

    if args.editor:
        global editor
        editor = args.editor[0]

    curses.wrapper(loop)


if __name__ == "__main__":
    main()
