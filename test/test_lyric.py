#!/usr/bin/python

import unittest
from lyrpy.lyric import Lyric, Verse


class TestLyric(unittest.TestCase):

    def setUp(self):
        self.l = Lyric('blink-182', 'Happy Days')
        self.l.generate_lyric()


    def test_verse(self):
        song_verse, v = self.l.sync_verse(104)
        self.assertEqual(song_verse.get_time(), 103.63)
        self.assertEqual(song_verse.get_verse(), "And I don't know if I'm ready to change")


if __name__ == '__main__':
    unittest.main()
