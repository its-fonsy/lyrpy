#!/usr/bin/python

from .ui import UI
from .lyric import Lyric
from . import lyrics_folder # variable

from os import listdir
from os.path import isfile, join
from mpd import MPDClient


def main():
    # Connect to MPD server
    client = MPDClient()
    client.timeout = None
    client.idletimeout = None
    client.connect("localhost", 6600)

    # Start the UI
    ui = UI()

    # Folder with all lyrics files
    lyrics_files = [f for f in listdir(lyrics_folder) if isfile(join(lyrics_folder, f))]

    artist = client.currentsong()['artist']
    title = client.currentsong()['title']
    song = Lyric(artist, title)    

    if song.filename() in lyrics_files:
        song.generate_lyric()

    while (1):
        artist = client.currentsong()['artist']
        title = client.currentsong()['title']

        if(client.status()['state'] in ['play', 'pause']):

            # getting info of the current song
            song_time = float(client.status()['elapsed'])
            song_dur = float(client.status()['duration'])
            cur_song = Lyric(artist, title)

            if cur_song.filename() in lyrics_files:

                # update the song if changes
                if song != cur_song:
                    song = cur_song
                    song.generate_lyric()

                # Print the lyric
                ui.write_lyric(song_time, song)
                ui.write_song_info(song_time, song_dur, song)

            else:
                ui.write_no_lyrics_message()
                ui.write_song_info(song_time, song_dur, song)

        if ui.key_pressed() == ord('q'):
            break

    # kill the UI
    ui.kill()

    # close MPD client
    client.close()
    client.disconnect()


if __name__ == "__main__":
    main()
