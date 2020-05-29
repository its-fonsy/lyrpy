#!/usr/bin/python

import curses

import requests
from bs4 import BeautifulSoup

artist = ''
title = ''
menu = []
base_url = "https://syair.info"

def search_url(artist, title):
    # url = "https://syair.info/search?q=bring+me+the+horizon"

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

def print_lyric(stdscr, lyric):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    y = 4
    for line in lyric.split('\n'):
        stdscr.addstr(y, 5, line)
        y += 1
        if y > (h - 5):
            break


def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()


def print_menu_title(stdscr):

    num_rows, num_cols = stdscr.getmaxyx()
    y = num_rows//2 - len(menu)//2 - 2

    msg = "Result for "
    song_msg = artist + ' - ' + title
    len_msg = len(msg) + len(song_msg)

    stdscr.addstr(y, num_cols//2 - len_msg//2, msg)
    stdscr.addstr(y, num_cols//2 - len_msg//2 + len(msg), song_msg, curses.A_BOLD)


def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    stdscr.refresh()


def print_searching_msg(stdscr):
    # Clear the screen
    stdscr.clear()
    num_rows, num_cols = stdscr.getmaxyx()

    msg = "Searching lyric for "
    song_msg = artist + ' - ' + title + '...'
    len_msg = len(msg) + len(song_msg)

    stdscr.addstr(num_rows // 2 - 1 , num_cols//2 - len_msg//2, msg)
    stdscr.addstr(num_rows // 2 - 1 , num_cols//2 - len_msg//2 + len(msg), song_msg, curses.A_BOLD)

def loop(stdscr):

    # getch() is blocking by default, with these func. just wait 150ms
    stdscr.nodelay(1)
    stdscr.timeout(150)
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    song_selected = False

    print_searching_msg(stdscr)
    stdscr.box()
    stdscr.refresh()

    global menu
    url = search_url(artist, title)
    lyrics_list = result_list(url)

    menu = []
    current_row = 0
    for lyric in lyrics_list:
        menu.append(lyric[0])
    menu.append('EXIT')

    while(1):
        key = stdscr.getch()

        num_rows, num_cols = stdscr.getmaxyx()
        # Clear the screen
        for i in range(num_rows):
            stdscr.move(i, 0)
            stdscr.clrtoeol()

        if (key == curses.KEY_UP or key == ord('k')) and current_row > 0:
            current_row -= 1
        elif (key == curses.KEY_DOWN or key == ord('j')) and current_row < len(menu)-1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # print_center(stdscr, "You selected '{}'".format(menu[current_row]))
            # print_center(stdscr, current_row)

            song_selected = True
            href = lyrics_list[current_row][1]
            lyric = lyric_fetch(href)

            # if user selected last row, exit the program
            if current_row == len(menu)-1:
                break

        if song_selected:
            print_lyric(stdscr, lyric)
        else:
            print_menu(stdscr, current_row)
            print_menu_title(stdscr)

        stdscr.box()
        stdscr.refresh()

        if ( key == ord('q') ):
            # Press 'q' to exit
            break




def main(art, tit):

    global artist
    artist = art
    global title
    title = tit

    curses.wrapper(loop)

