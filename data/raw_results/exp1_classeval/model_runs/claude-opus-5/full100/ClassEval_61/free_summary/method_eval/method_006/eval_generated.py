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
            if self.current_song == song:
                self.stop()
            self.playlist.remove(song)

    def play(self):
        if self.playlist and self.current_song:
            return self.playlist[0]
        return False

    def stop(self):
        if self.current_song is not None:
            self.current_song = None
            return True
        return False

    def switch_song(self):
        if self.current_song is None:
            return False
        current_index = self.playlist.index(self.current_song)
        if current_index >= len(self.playlist) - 1:
            return False
        self.current_song = self.playlist[current_index + 1]
        return True

    def previous_song(self):
        if self.current_song is None:
            return False
        current_index = self.playlist.index(self.current_song)
        if current_index <= 0:
            return False
        self.current_song = self.playlist[current_index - 1]
        return True

    def set_volume(self, volume):
        if volume < 0 or volume > 100:
            return False
        self.volume = volume

    def shuffle(self):
        if not self.playlist:
            return False
        random.shuffle(self.playlist)
        return True

import unittest

class MusicPlayerTestSetVolume(unittest.TestCase):
    def test_set_volume(self):
        musicPlayer = MusicPlayer()
        self.assertEqual(musicPlayer.set_volume(50), None)
        self.assertEqual(musicPlayer.volume, 50)

    def test_set_volume2(self):
        musicPlayer = MusicPlayer()
        self.assertEqual(musicPlayer.set_volume(100), None)
        self.assertEqual(musicPlayer.volume, 100)

    def test_set_volume3(self):
        musicPlayer = MusicPlayer()
        self.assertEqual(musicPlayer.set_volume(0), None)
        self.assertEqual(musicPlayer.volume, 0)

    def test_set_volume4(self):
        musicPlayer = MusicPlayer()
        self.assertEqual(musicPlayer.set_volume(101), False)
        self.assertEqual(musicPlayer.volume, 50)

    def test_set_volume5(self):
        musicPlayer = MusicPlayer()
        self.assertEqual(musicPlayer.set_volume(-1), False)
        self.assertEqual(musicPlayer.volume, 50)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
