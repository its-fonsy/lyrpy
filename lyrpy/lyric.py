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
        self.lyric = []

    def generate_lyric(self):

        with open(lyrics_folder + '/' + self.filename(), 'r') as lyric_file:
            for line in lyric_file:

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
                        self.lyric.append(Verse(minute, sec, verse))

        # sort the lyrics
        self.lyric.sort()


    def singed_verse(self, time):

        ts = self.lyric[0].get_time()

        if ( time < ts ):
            return self.lyric[0].get_time(), 0

        i = 0
        for verse in self.lyric:
            ts = verse.get_time()
            if (time < ts):
                return self.lyric[i-1], i-1
            i += 1

        return self.lyric[len(self.lyric) - 1], len(self.lyric) - 1


    def get_info(self):
        return self.artist, self.title


    def filename(self):
        return self.artist + ' - ' + self.title + '.lrc'


    def line(self, i):
        return str(self.lyric[i].get_verse())


    def __eq__(self, other):
        if isinstance(other, Lyric):
            return (self.artist == other.artist) and (self.title == other.title)
        return False


    def __str__(self):
        return f"{self.artist} - {self.title}"
