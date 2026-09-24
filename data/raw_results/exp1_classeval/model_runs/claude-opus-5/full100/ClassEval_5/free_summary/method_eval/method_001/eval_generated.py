class AutomaticGuitarSimulator:
    def __init__(self, play_text):
        self.play_text = play_text

    def interpret(self, display=False):
        if not self.play_text or not self.play_text.strip():
            return []

        segments = []
        for token in self.play_text.split(' '):
            # Find where the leading alphabetic prefix ends
            split_index = 0
            for char in token:
                if char.isalpha():
                    split_index += 1
                else:
                    break

            chord = token[:split_index]
            tune = token[split_index:]

            segment = {'Chord': chord, 'Tune': tune}
            segments.append(segment)

            if display:
                self.display(chord, tune)

        return segments

    def display(self, key, value):
        return "Normal Guitar Playing -- Chord: {}, Play Tune: {}".format(key, value)

import unittest

class AutomaticGuitarSimulatorTestDisplay(unittest.TestCase):
    def test_display_1(self):
        context = AutomaticGuitarSimulator("C53231323 Em43231323")
        play_list = context.interpret()
        str = context.display(play_list[0]['Chord'], play_list[0]['Tune'])
        self.assertEqual(str, "Normal Guitar Playing -- Chord: C, Play Tune: 53231323")

    def test_display_2(self):
        context = AutomaticGuitarSimulator("C53231323 Em43231323")
        play_list = context.interpret()
        str = context.display(play_list[1]['Chord'], play_list[1]['Tune'])
        self.assertEqual(str, "Normal Guitar Playing -- Chord: Em, Play Tune: 43231323")

    def test_display_3(self):
        context = AutomaticGuitarSimulator("F43231323 G63231323")
        play_list = context.interpret()
        str = context.display(play_list[0]['Chord'], play_list[0]['Tune'])
        self.assertEqual(str, "Normal Guitar Playing -- Chord: F, Play Tune: 43231323")

    def test_display_4(self):
        context = AutomaticGuitarSimulator("F43231323 G63231323")
        play_list = context.interpret()
        str = context.display(play_list[1]['Chord'], play_list[1]['Tune'])
        self.assertEqual(str, "Normal Guitar Playing -- Chord: G, Play Tune: 63231323")

    def test_display_5(self):
        context = AutomaticGuitarSimulator("")
        str = context.display('', '')
        self.assertEqual(str, "Normal Guitar Playing -- Chord: , Play Tune: ")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
