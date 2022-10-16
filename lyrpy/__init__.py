# Place holder
import argparse
import os

try:
    lyrics_folder = os.environ['LYRICS_DIR']
except:
    pass

# Read argparse
parser = argparse.ArgumentParser( \
            description='Display sync lyric of the current playing song on mpd server')

parser.add_argument('-d', '--lyrics-dir', nargs=1, \
                     help="Specify the location of the lyrics directory")
parser.add_argument('-e', '--editor', nargs=1 , \
                     help="Specify the editor to use to modify lyrics file")

# Args overwrite the config file
args = parser.parse_args()
if args.lyrics_dir:
    lyrics_folder = args.lyrics_folder[0]

if args.editor:
    editor = args.editor[0]

if lyrics_folder is None:
    print("Set environment variable LYRICS_DIR to set the lyrics directory")
    print('or use the "-d LYRICS_DIR" flag')

if lyrics_folder[-1] != '/':
    lyrics_folder += '/'

