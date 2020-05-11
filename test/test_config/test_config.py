#!/usr/bin/python

import unittest
import config

class TestConfig(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read(self):
        cfg = config.read()
        self.assertIsNotNone(cfg['Default']['editor'])
        self.assertIsNotNone(cfg['Default']['lyrics_directory'])


if __name__ == '__main__':
    unittest.main()
