# Introduction
`lyrpy` is a terminal application to display the lyric of a song played on the `mpd server`. It's based on
`Python3` and `ncurses` and has the ability to highlight the verse that is being singed.

![lyrpy](doc/img/lyrpy.png)

### Requirements

+ GNU Linux as Operative System
+ `mpd` package installed
+ `python3.8` (or greater) and `pip`

### Installation
Clone the repo and run the installer.

	$ git clone https://github.com/its-fonsy/lyrpy
	$ cd lyrpy
	$ python3 setup.py install

If it gives error's use the magic word `sudo` on the last comand.

## Usage
Simply run

	$ lyrpy

The folder with all the lyrycs files can be set in the `$HOME/.config/lyrpy/lyrpy.conf` file, or
launching it with the flag

	$ lyrpy -d LYRYCS_DIR

When `lyrpy` is running

+ pressing `q` will quit the program
+ pressing `o` will open the current lyrics in a text editor

The text editor can be set in the `lyrpy.conf` or with the flag

	$ lyrpy -e EDITOR

