#!/usr/bin/python

class Verse:
    def __init__(self, _minute, _sec, _verse):
        self.minute = _minute
        self.second = _sec
        self.verse = _verse

    def __lt__(self, other):
        if self.minute == other.minute:
            return self.second < other.second
        else:
            return self.minute < other.minute

    def get_verse(self):
        return self.verse

    def get_time(self):
        # The time is returned in seconds
        # Example: '2:25.00' is returned as '145.00'
        return float(self.minute*60) + self.second

    def __str__(self):
        return f"Minute:{self.minute} \t Second:{self.second}\nVerse:{self.verse}"
