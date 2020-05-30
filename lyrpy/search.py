#!/usr/bin/python

import curses
import requests
from . import lyrics_folder
from bs4 import BeautifulSoup

menu = []
base_url = "https://syair.info"

def search_url(artist, title):
    # Generate the url to search in the site
    artist = '+'.join(artist.lower().split())
    title = '+'.join(title.lower().split())
    url = base_url + '/search?q=' + artist + '+' + title
    return url


def result_list(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    # Generate the list of the lyrics
    lyric_list = []
    for link in soup.find_all('a', class_='title'):
        link_href = link.get('href')
        link_content = link.contents[0]
        lyric_list.append([link_content, link_href])

    return lyric_list


def lyric_fetch(href):
    url = base_url + href
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    # r = open('lyric_page.html', 'r')
    # soup = BeautifulSoup(r.read(), 'lxml')
    # r.close()

    lyric_html = soup.find('div', class_='entry')
    lyric = lyric_html.get_text()
    lyric = lyric.split('Published')
    return str(lyric[0])


def syair(artist, title):
    url = search_url(artist, title)
    lyric_list = result_list(url)

    ans = ''
    while ans != 'y':

        i=1
        for item in lyric_list:
            print(f"{i}: {item[0]}")
            i += 1

        n = int(input('Choose the lyric (n): '))

        url_lyric_page = base_url + lyric_list[n-1][1]
        lyric = lyric_fetch(url_lyric_page)
        print(lyric)
        ans = input("Do you like this lyric [y/n, q to quit]? ")

        if ans == 'q':
            break

    if ans == 'y':
        lyric_file = open(artist + ' - ' + title + '.lrc', 'w')
        lyric_file.write(lyric)
        lyric_file.close()


def print_lyric(stdscr, lyric, current_row):
    stdscr.clear()

    n_rows, n_cols = stdscr.getmaxyx()
    offset = 3

    lyric_len = len(lyric)

    if lyric_len < n_rows:
        idx_end = lyric_len - 2*offset
    else:
        idx_end = n_rows - 2*offset

        if current_row + idx_end >= lyric_len:
            current_row = lyric_len - idx_end

    for idx in range(idx_end):
        stdscr.addstr(idx + offset, offset, lyric[current_row + idx])


def print_menu_title(stdscr, artist, title):

    num_rows, num_cols = stdscr.getmaxyx()
    y = num_rows//2 - len(menu)//2 - 2

    msg = "Result for "
    song_msg = artist + ' - ' + title
    len_msg = len(msg) + len(song_msg)

    stdscr.addstr(y, num_cols//2 - len_msg//2, msg)
    stdscr.addstr(y, num_cols//2 - len_msg//2 + len(msg), song_msg, curses.A_BOLD)


def print_menu(stdscr, selected_row_idx):
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        if len(row) > (w-10):
            row = row[:w-10] + '...'
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)


def print_searching_msg(stdscr, artist, title):
    # Clear the screen
    stdscr.clear()
    num_rows, num_cols = stdscr.getmaxyx()

    msg = "Searching lyric for "
    song_msg = artist + ' - ' + title + '...'
    len_msg = len(msg) + len(song_msg)

    stdscr.addstr(num_rows // 2 - 1 , num_cols//2 - len_msg//2, msg)
    stdscr.addstr(num_rows // 2 - 1 , num_cols//2 - len_msg//2 + len(msg), song_msg, curses.A_BOLD)


def print_saving_msg(stdscr):
    # Clear the screen
    stdscr.clear()
    num_rows, num_cols = stdscr.getmaxyx()

    msg = "Saving the lyric to "
    len_msg = len(msg) + len(lyrics_folder)

    stdscr.addstr(num_rows // 2 - 1 , num_cols//2 - len_msg//2, msg)
    stdscr.addstr(num_rows // 2 - 1 , num_cols//2 - len_msg//2 + len(msg), lyrics_folder, curses.A_BOLD)
    conf_msg = 'Confirm? (y/n)'
    stdscr.addstr(num_rows // 2, num_cols//2 - len(conf_msg)//2, conf_msg)

    stdscr.refresh()


def print_help_msg(stdscr, song_selected):
    stdscr.clear()
    num_rows, num_cols = stdscr.getmaxyx()
    max_len_msg = 46
    x = num_cols//2 - max_len_msg//2
    y = num_rows//2 - 4

    # Writing up message
    stdscr.addstr(y,    x, "Press")
    stdscr.addstr(y,  x+6, "k", curses.A_BOLD)
    stdscr.addstr(y,  x+8, "or")
    stdscr.addstr(y, x+11, "UP_ARROW", curses.A_BOLD)
    if song_selected:
        stdscr.addstr(y, x+20, "to scroll up the lyric")
    else:
        stdscr.addstr(y, x+20, "to move up in the menu")

    # Writing down message
    stdscr.addstr(y+1,    x, "Press")
    stdscr.addstr(y+1,  x+6, "j", curses.A_BOLD)
    stdscr.addstr(y+1,  x+8, "or")
    stdscr.addstr(y+1, x+11, "DOWN_ARROW", curses.A_BOLD)
    if song_selected:
        stdscr.addstr(y+1, x+22, "to scroll down the lyric")
    else:
        stdscr.addstr(y+1, x+22, "to move down in the menu")

    # Writing ENTER message
    stdscr.addstr(y+2,    x, "Press")
    stdscr.addstr(y+2,  x+6, "ENTER", curses.A_BOLD)
    if song_selected:
        stdscr.addstr(y+2, x+12, "to save the lyric")
    else:
        stdscr.addstr(y+2, x+12, "to select a lyric")

    # Writing quit message
    stdscr.addstr(y+3,   x, "Press")
    stdscr.addstr(y+3, x+6, "q", curses.A_BOLD)
    if song_selected:
        stdscr.addstr(y+3, x+8, "to select another lyric")
    else:
        stdscr.addstr(y+3, x+8, "to return viewing the lyric")

    ## Drawing the box
    pad = 2

    # Top line
    stdscr.addstr(y - pad, x - pad + 1, "─"*( max_len_msg + pad ))
    # Top-left corner
    stdscr.addstr(y - pad, x - pad, "┌")
    # Top-right corner
    stdscr.addstr(y - pad, x + pad + max_len_msg - 1, "┐")

    # Bottom line
    stdscr.addstr(y + 3 + pad, x - pad + 1, "─"*( max_len_msg + pad ))
    # Bottom-left corner
    stdscr.addstr(y + 3 + pad, x - pad, "└")
    # Bottom-right corner
    stdscr.addstr(y + 3 + pad, x + pad + max_len_msg - 1, "┘")

    # Left line
    for i in range(y-pad + 1, y + 3 + pad):
        stdscr.addstr(i, x - pad, "│")

    # Right line
    for i in range(y-pad + 1, y + 3 + pad):
        stdscr.addstr(i, x + pad + max_len_msg - 1, "│")


    x_help = num_cols//2 - len("help")//2
    stdscr.addstr(y - pad, x_help, "HELP", curses.A_BOLD)
    x_hlp_exit = num_cols//2 - len("Press any key to exit from the help")//2
    stdscr.addstr(y+3+pad, x_hlp_exit, "Press any key to exit from the help")

    stdscr.refresh()

    stdscr.nodelay(0)
    key = stdscr.getch()
    stdscr.nodelay(1)



def loop(stdscr, artist, title):

    # getch() is blocking by default, with these func. just wait 150ms
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    song_selected = False

    # Clear the screen and display the searching message
    stdscr.clear()
    print_searching_msg(stdscr, artist, title)
    stdscr.box()
    stdscr.refresh()

    # Create the menu
    global menu
    menu = []
    current_row = 0

    # while len(menu) == 0:
    # Get a list of found lyrics
    url = search_url(artist, title)
    lyrics_list = result_list(url)

    for lyric in lyrics_list:
        menu.append(lyric[0])
    menu.append('EXIT')

    while(1):

        key = stdscr.getch()
        stdscr.clear()

        num_rows, num_cols = stdscr.getmaxyx()

        if not song_selected:
            if (key == curses.KEY_UP or key == ord('k')) and current_row >= 0:
                current_row -= 1

                # If on the first item on the menu, press up to got to the last
                if current_row < 0:
                    current_row = len(menu) - 1

            elif (key == curses.KEY_DOWN or key == ord('j')) and current_row <= len(menu)-1:
                current_row += 1

                # If on the last item on the menu, press down to got to the first
                if current_row == len(menu):
                    current_row = 0

            elif key == curses.KEY_ENTER or key in [10, 13]:

                # if user selected last row, exit the program
                if current_row == len(menu)-1:
                    break

                # User has select a menu entry
                song_selected = True
                href = lyrics_list[current_row][1]
                lyric = lyric_fetch(href)
                lyric = lyric.split('\n')
                current_row = 0

            print_menu(stdscr, current_row)
            print_menu_title(stdscr, artist, title)

        else:
            if (key == curses.KEY_UP or key == ord('k')) and current_row > 0:
                current_row -= 1
            elif (key == curses.KEY_DOWN or key == ord('j')):
                if current_row < (len(lyric) - num_rows + 6):
                    current_row += 1

            elif key == curses.KEY_ENTER or key in [10, 13]:
                print_saving_msg(stdscr)
                stdscr.nodelay(0)
                key = stdscr.getch()
                stdscr.nodelay(1)
                if key == ord('y'):
                    lyric_file = open(lyrics_folder + artist + ' - ' + title + '.lrc', 'w')
                    for line in lyric:
                        lyric_file.write(line + '\n')
                    lyric_file.close()
                    break

            print_lyric(stdscr, lyric, current_row)

        stdscr.box()
        stdscr.refresh()


        if ( key == ord('q') ):
            if song_selected:
                song_selected = False
                current_row = 0
            else:
                break

        if ( key == ord('?') ):
            print_help_msg(stdscr, song_selected)
