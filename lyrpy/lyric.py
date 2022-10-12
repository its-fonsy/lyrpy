#!/usr/bin/python

# Display the lyrics of the song is playing on MPD, with sync

import re
from . import lyrics_folder

class Verse:
    def __init__(self, _minute, _sec, _verse):
        self.minute = _minute
        self.second = _sec
        self.verse = _verse

    def __lt__(self, other):
        if self.minute == other.minute:
            return self.second < other.second
        else:
            return self.minute < other.minute

    def get_verse(self):
        return self.verse

    def get_time(self):
        # The time is returned in seconds
        # Example: '2:25.00' is returned as '145.00'
        return float(self.minute*60) + self.second

    def __str__(self):
        return f"Minute:{self.minute} \t Second:{self.second}\nVerse:{self.verse}"


class Lyric:
    def __init__(self, _artist, _title):
        self.artist = _artist
        self.title = _title

    def generate_lyric(self):
        self.song_lyric = []

        with open(lyrics_folder + '/' + self.filename(), 'r') as lyric_data:
            for line in lyric_data:

                if re.search("^\[00:00.00\][A-Z,a-z]", line) or \
                   re.search("^\[[A-Z,a-z]", line) or \
                   line == '\n':
                       # Exclude lines like:
                       #    - '[00:00.00]Artist: ARTITST_NAME' or similar
                       #    - '[alb: ALBUM_NAME]' or general metadata
                       #    - newline
                    pass
                else:
                    # Get the time stamp
                    time_stamps = re.findall("\[\d\d:\d\d\.\d\d\]", line)

                    # Get the verse of the line
                    verse = ''
                    for ch in reversed(line):
                        if ch == ']':
                            break
                        verse += ch
                    verse = verse[::-1].strip()
                    # print(verse)

                    # Add the data with the Verse class to the lyric list
                    for stamp in time_stamps:
                        stamp = stamp[1:-1]
                        minute, sec = stamp.split(':')
                        minute = int(minute)
                        sec = float(sec)
                        self.song_lyric.append(Verse(minute, sec, verse))

        # sort the lyrics
        self.song_lyric.sort()


    def sync_verse(self, time):

        # Return the verse that is being singed
        for v in range(len(self.song_lyric) - 1):
            if v != (len(self.song_lyric) - 1) and \
               (time - self.song_lyric[v].get_time()) > 0.0 and \
               (time - self.song_lyric[v+1].get_time()) < 0.0:
                   return self.song_lyric[v], v

        if (time - self.song_lyric[0].get_time()) < 0.0:
            return self.song_lyric[0], 0
        else:
            return self.song_lyric[len(self.song_lyric) - 1], len(self.song_lyric) - 1


    def get_info(self):
        return self.artist, self.title


    def filename(self):
        return self.artist + ' - ' + self.title + '.lrc'


    def lenght(self):
        return len(self.song_lyric)


    def line(self, i):
        return str(self.song_lyric[i].get_verse())

    def __eq__(self, other):
        if isinstance(other, Lyric):
            return (self.artist == other.artist) and (self.title == other.title)
        return False


    def __str__(self):
        return f"{self.artist} - {self.title}"
