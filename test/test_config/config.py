#!/usr/bin/python

from configparser import ConfigParser
import os

# TODO
# 1. Is the ~/.config/lyrpy dir exhist?
# 2. If so read the config, else generate a basic one

def read():
    HOME = os.environ['HOME']
    config_dir = HOME + '/.config/'

    if 'lyrpy' in os.listdir(config_dir):
        config_dir = config_dir + 'lyrpy'
    else:
        os.mkdir(config_dir + 'lyrpy')
        config_dir = config_dir + 'lyrpy'

    config = ConfigParser()

    os.chdir(config_dir)
    if 'lyrpy.conf' in os.listdir():
        config.read('lyrpy.conf')
    else:
        config['Default'] = { 'editor' : 'nvim',
                              'lyrics_directory' : '~/musica/lyrics' }

        with open('lyrpy.conf', 'w') as config_file:
            config.write(config_file)

    return config
