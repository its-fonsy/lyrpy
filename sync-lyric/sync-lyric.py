#!/usr/bin/python

import argparse
import ui
import curses

def main():
    parser = argparse.ArgumentParser(description='Display sync lyric of the current playing song on mpd server')

    parser.add_argument('-lf', '--lyrics-folder', nargs=1, help="Specify the location of the lyrics folder")

    args = parser.parse_args()

    if args.lyrics_folder:
        lyrics_folder = args.lyrics_folder[0]

    curses.wrapper(ui.ui)


if __name__ == "__main__":
    main()
