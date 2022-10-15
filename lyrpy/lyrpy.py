#!/usr/bin/env python3

from .ui import UI
from .lyric import Lyric
from . import lyrics_folder # constant
from .cmus_client import cmus_get_artist, cmus_get_title, cmus_get_time, cmus_get_dur

from os import listdir
from os.path import isfile, join
from mpd import MPDClient
from pycmus import remote


def main():

    # Try to connect to MPD server
    try:
        # Connect to MPD server
        mpd_client = MPDClient()
        mpd_client.timeout = None
        mpd_client.idletimeout = None
        mpd_client.connect("localhost", 6600)

        client = 'mpd'
    except ConnectionError:
        # Try to connect to CMUS
        cmus = remote.PyCmus()
        client = 'cmus'
    except:
        print("Nor MPD/CMUS server is running :(")
        exit(-1)

    # Start the UI
    ui = UI()

    # Folder with all lyrics files
    lyrics_files = [f for f in listdir(lyrics_folder) if isfile(join(lyrics_folder, f))]
    song = Lyric('dummy', 'song')

    while (1):

        # getting info of the current song
        if client == "mpd":
            artist = mpd_client.currentsong()['artist']
            title = mpd_client.currentsong()['title']
            song_time = float(mpd_client.status()['elapsed'])
            song_dur = float(mpd_client.status()['duration'])
        elif client == "cmus":
            s = cmus.status()
            artist = cmus_get_artist(s)
            title = cmus_get_title(s)
            song_time = float(cmus_get_time(s)) + 2.0
            song_dur = float(cmus_get_dur(s))

        cur_song = Lyric(artist, title)

        if cur_song.filename() in lyrics_files:

            # update the song if changes
            if song != cur_song:
                song = cur_song
                song.generate_lyric()

            # Print the lyric
            ui.print_lyric(song_time, song)

        else:
            ui.write_no_lyrics_message()
            # ui.write_debug_message(cur_song.filename())

        ui.write_song_info(song_time, song_dur, cur_song)

        if ui.key_pressed() == ord('q'):
            break

    # kill the UI
    ui.kill()

    # close MPD mpd_client
    if client == "mpd":
        mpd_client.close()
        mpd_client.disconnect()


if __name__ == "__main__":
    main()
