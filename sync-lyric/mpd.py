# This file contains all the mpd-client function related

import mpd

def connect_client():
    client = mpd.MPDClient()
    client.timeout = None
    client.idletimeout = None
    client.connect("localhost", 6600)
    return client


def disconnect_client(client):
    client.close()
    client.disconnect
