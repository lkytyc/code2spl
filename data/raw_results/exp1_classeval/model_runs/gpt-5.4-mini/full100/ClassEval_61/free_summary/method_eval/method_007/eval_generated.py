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
        if self.playlist and self.current_song is not None:
            return self.playlist[0]
        if self.playlist:
            return False

    def stop(self):
        if self.current_song is not None:
            self.current_song = None
            return True
        return False

    def switch_song(self):
        if self.current_song is None:
            return False
        if self.current_song not in self.playlist:
            return False
        index = self.playlist.index(self.current_song)
        if index + 1 < len(self.playlist):
            self.current_song = self.playlist[index + 1]
            return True
        return False

    def previous_song(self):
        if self.current_song is None:
            return False
        if self.current_song not in self.playlist:
            return False
        index = self.playlist.index(self.current_song)
        if index - 1 >= 0:
            self.current_song = self.playlist[index - 1]
            return True
        return False

    def set_volume(self, volume):
        if 0 <= volume <= 100:
            self.volume = volume
            return
        return False

    def shuffle(self):
        if not self.playlist:
            return False
        import random
        random.shuffle(self.playlist)
        return True

import unittest

class MusicPlayerTestShuffle(unittest.TestCase):
    def test_shuffle(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = ["song1", "song2"]
        self.assertEqual(musicPlayer.shuffle(), True)

    def test_shuffle_2(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = []
        musicPlayer.current_song = "song1"
        self.assertEqual(musicPlayer.shuffle(), False)

    def test_shuffle_3(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = ["song1", "song2"]
        musicPlayer.current_song = "song2"
        self.assertEqual(musicPlayer.shuffle(), True)

    def test_shuffle_4(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = ["song1", "song2"]
        musicPlayer.current_song = "song3"
        self.assertEqual(musicPlayer.shuffle(), True)

    def test_shuffle_5(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = ["song1", "song2"]
        musicPlayer.current_song = "song1"
        self.assertEqual(musicPlayer.shuffle(), True)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
