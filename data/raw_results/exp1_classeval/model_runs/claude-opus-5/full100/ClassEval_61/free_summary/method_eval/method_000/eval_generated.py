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

class MusicPlayerTestAddSong(unittest.TestCase):
    def test_add_song(self):
        musicPlayer = MusicPlayer()
        musicPlayer.add_song("song1")
        self.assertEqual(musicPlayer.playlist, ["song1"])

    def test_add_song2(self):
        musicPlayer = MusicPlayer()
        musicPlayer.add_song("song1")
        musicPlayer.add_song("song2")
        self.assertEqual(musicPlayer.playlist, ["song1", "song2"])

    def test_add_song3(self):
        musicPlayer = MusicPlayer()
        musicPlayer.add_song("song1")
        musicPlayer.add_song("song2")
        musicPlayer.add_song("song3")
        self.assertEqual(musicPlayer.playlist, ["song1", "song2", "song3"])

    def test_add_song4(self):
        musicPlayer = MusicPlayer()
        musicPlayer.add_song("song1")
        musicPlayer.add_song("song2")
        musicPlayer.add_song("song3")
        musicPlayer.add_song("song4")
        self.assertEqual(musicPlayer.playlist, ["song1", "song2", "song3", "song4"])

    def test_add_song5(self):
        musicPlayer = MusicPlayer()
        musicPlayer.add_song("song1")
        musicPlayer.add_song("song2")
        musicPlayer.add_song("song3")
        musicPlayer.add_song("song4")
        musicPlayer.add_song("song5")
        self.assertEqual(musicPlayer.playlist, ["song1", "song2", "song3", "song4", "song5"])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
