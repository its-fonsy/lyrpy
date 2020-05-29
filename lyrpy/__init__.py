# Place holder
import argparse
from . import config

# Read the config file in $HOME/.config/lyrpy
lyr_config = config.read()
lyrics_folder = lyr_config['Default']['lyrics_directory']
editor = lyr_config['Default']['editor']

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
