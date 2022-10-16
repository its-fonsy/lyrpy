## Introduction
lyrpy is a terminal application that displays the lyric of a song played by
`mpd` or `cmus`. It's based on `python3` and `ncurses` and has the ability to
highlight the verse that is being singed.

![lyrpy](doc/img/lyrpy.gif)


## Installation
To install `lyrpy` you first need to clone this repo

	$ git clone https://github.com/its-fonsy/lyrpy
	$ cd lyrpy

Then you can install it for everyone

	$ sudo python3 setup.py install

or just for you

	$ python3 setup.py install --user


## Setup
After the installation you have to set and environment variable with the path
of all your lyrics files

	$ export LYRICS_DIR="/full/path/to/lyrics/dir/" >> ~/.profile
	$ source ~/.profile

(if you don't want to set it up then you can run `lyrpy` with the flag `-d`)
	

## Usage
Simply run

	$ lyrpy

now the program will look for `.lrc` files that matches the song being played by the music player.


## Lyrics Files
To match the song that is playing the files must be named like so

	ARTIST - TITLE.lrc

The selection of the lyric files is based on the metadata of the played song.
`lyrpy` shows on the bottom-left the author and title of the track that is
being played (see the image above).

The `.lrc` files must be similar to this

```
[ti:Numb]
[ar:Linkin park]
[length:03:07]

[00:00.00]
[00:21.88]I'm tired of being what you want me to be
[00:25.78]Feeling so faithless, lost under the surface
[00:29.75]
[00:30.55]I don't know what you're expecting of me
[00:34.11]Put under the pressure,
[00:39.02]of walking in your shoes
[00:39.22]Caught in the undertow,
[00:40.22]just caught in the undertow
[00:42.28]Every step that I take
....
```
**Timestamp are required**

For example if you are listening *Numb* by *Linkin Park* the file must be named

	Linkin Park - Numb.lrc


## Problems
+ right now lyrpy doesn't support `offset`, so use lyrics without it
