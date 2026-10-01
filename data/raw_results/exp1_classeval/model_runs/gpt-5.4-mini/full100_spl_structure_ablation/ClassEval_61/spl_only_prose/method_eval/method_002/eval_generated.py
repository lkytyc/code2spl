class MusicPlayer:
    def __init__(self):
        self.playlist = []
        self.current_song = None
        self.volume = 50

    def add_song(self, song):
        self.playlist.append(song)

    def play(self):
        condition_result = bool(self.playlist) and bool(self.current_song)
        if condition_result:
            return self.playlist[0]
        return False

    def previous_song(self):
        has_current_song = bool(self.current_song)
        if not has_current_song:
            return False

        current_index = self.playlist.index(self.current_song)
        has_previous_song = current_index > 0
        if has_previous_song:
            self.current_song = self.playlist[current_index - 1]
            return True
        return False

    def remove_song(self, song):
        presence_check = song in self.playlist
        if presence_check:
            self.playlist.remove(song)
            is_current_song = self.current_song == song
            if is_current_song:
                self.stop()

    def set_volume(self, volume):
        is_valid_volume = 0 <= volume <= 100
        if is_valid_volume:
            self.volume = volume
        else:
            return False

    def shuffle(self):
        playlist_present = bool(self.playlist)
        if playlist_present:
            import random
            random.shuffle(self.playlist)
            return True
        return False

    def stop(self):
        condition_met = bool(self.current_song)
        if condition_met:
            self.current_song = None
            return True
        return False

    def switch_song(self):
        has_current_song = bool(self.current_song)
        if not has_current_song:
            return False

        current_index = self.playlist.index(self.current_song)
        has_next_song = current_index < len(self.playlist) - 1
        if has_next_song:
            self.current_song = self.playlist[current_index + 1]
            return True
        return False

import unittest

class MusicPlayerTestPlay(unittest.TestCase):
    def test_play(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = ["song1", "song2"]
        musicPlayer.current_song = "song1"
        self.assertEqual(musicPlayer.play(), "song1")

    def test_play_2(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = []
        musicPlayer.current_song = "song2"
        self.assertEqual(musicPlayer.play(), None)

    def test_play_3(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = ["song1", "song2"]
        self.assertEqual(musicPlayer.play(),False)

    def test_play_4(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = ["song1", "song2"]
        musicPlayer.current_song = "song3"
        self.assertEqual(musicPlayer.play(), "song1")

    def test_play_5(self):
        musicPlayer = MusicPlayer()
        musicPlayer.playlist = ["song1", "song2"]
        musicPlayer.current_song = "song1"
        self.assertEqual(musicPlayer.play(), "song1")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
