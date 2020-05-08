#!/usr/bin/python

# Display the lyrics of the song is playing on MPD, with sync

import re
from Verse import Verse


def get_lyric_data(lyric_file):
    lyric = []

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
                    lyric.append(Verse(minute, sec, verse))
    return lyric


def sync_verse(time, lyric):

    # Return the verse that is being singed
    for v in range(len(lyric) - 1):
        if v != (len(lyric) - 1) and \
           (time - lyric[v].get_time()) > 0.0 and \
           (time - lyric[v+1].get_time()) < 0.0:
               return lyric[v], v


def demo():
    lyric = get_lyric_data('blink-182 - Happy Days.lrc')
    lyric.sort()

    verse = sync_verse(104, lyric)
    print(verse.get_time())
    print(verse.get_verse())


if __name__ == '__main__':
    demo()

