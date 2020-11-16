#!/usr/bin/python

# Display the lyrics of the song is playing on MPD, with sync

import re


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


def get_lyric_data(lyric_file):
    song_lyric = []

    with open(lyric_file, 'r') as lyric_data:
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
                    song_lyric.append(Verse(minute, sec, verse))
    return song_lyric


def sync_verse(time, song_lyric):

    # Return the verse that is being singed
    for v in range(len(song_lyric) - 1):
        if v != (len(song_lyric) - 1) and \
           (time - song_lyric[v].get_time()) > 0.0 and \
           (time - song_lyric[v+1].get_time()) < 0.0:
               return song_lyric[v], v

    if (time - song_lyric[0].get_time()) < 0.0:
        return song_lyric[0], 0
    else:
        return song_lyric[len(song_lyric) - 1], len(song_lyric) - 1
