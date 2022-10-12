def cmus_get_artist( response ):
    for tag in (response.split('\n')):
        if 'tag artist' in tag:
            return tag[11:].replace('‐', '-')


def cmus_get_title( response ):
    for tag in (response.split('\n')):
        if 'tag title' in tag:
            return tag[10:].replace('‐', '-')


def cmus_get_time( response ):
    for tag in (response.split('\n')):
        if 'position' in tag:
            return int(tag[9:])


def cmus_get_dur( response ):
    for tag in (response.split('\n')):
        if 'duration' in tag:
            return int(tag[9:])
