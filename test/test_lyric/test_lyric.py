#!/usr/bin/python

import unittest
import lyric


class TestLyric(unittest.TestCase):

    def setUp(self):
        lyric_file = 'sample.lrc'
        self.song_lyric = lyric.get_lyric_data(lyric_file)
        self.song_lyric.sort()

    def tearDown(self):
        pass

    def test_lyric(self):
        # Checking just the lenght of the list
        self.assertEqual(len(self.song_lyric), 57)


    def test_verse(self):
        song_verse, v = lyric.sync_verse(104, self.song_lyric)
        self.assertEqual(song_verse.get_time(), 103.63)
        self.assertEqual(song_verse.get_verse(), "And I don't know if I'm ready to change")


if __name__ == '__main__':
    unittest.main()
