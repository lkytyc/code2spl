import random


class MusicPlayer:
    def __init__(self):
        self.playlist = []
        self.current_song = None
        self.volume = 50

    def add_song(self, song):
        self.playlist.append(song)

    def remove_song(self, song):
        if song in self.playlist:
            self.playlist.remove(song)
            if self.current_song == song:
                self.stop()

    def play(self):
        if self.playlist and self.current_song:
            return self.playlist[0]
        elif len(self.playlist):
            return False

    def stop(self):
        if self.current_song:
            self.current_song = None
            return True
        return False

    def switch_song(self):
        if self.current_song:
            current_index = self.playlist.index(self.current_song)
            if current_index < len(self.playlist) - 1:
                self.current_song = self.playlist[current_index + 1]
                return True
            return False
        return False

    def previous_song(self):
        if self.current_song:
            current_index = self.playlist.index(self.current_song)
            if current_index > 0:
                self.current_song = self.playlist[current_index - 1]
                return True
            return False
        return False

    def set_volume(self, volume):
        if not (0 <= volume <= 100):
            return False
        self.volume = volume

    def shuffle(self):
        if self.playlist:
            random.shuffle(self.playlist)
            return True
        return False

import unittest

class MusicPlayerTestPreviousSong(unittest.TestCase):
    def test_previous_song(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = ["song1", "song2", "song3"]
        musicPlayer.current_song = "song2"
        self.assertEqual(musicPlayer.previous_song(), True)

    def test_previous_song2(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = ["song1", "song2", "song3"]
        musicPlayer.current_song = "song1"
        self.assertEqual(musicPlayer.previous_song(), False)

    def test_previous_song3(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = ["song1", "song2", "song3"]
        musicPlayer.current_song = "song3"
        self.assertEqual(musicPlayer.previous_song(), True)

    def test_previous_song4(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = ["song1", "song2", "song3"]
        self.assertEqual(musicPlayer.previous_song(), False)

    def test_previous_song5(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = []
        self.assertEqual(musicPlayer.previous_song(), False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
