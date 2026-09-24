class AutomaticGuitarSimulator:
    def __init__(self, play_text):
        self.play_text = play_text

    def display(self, chord, tune):
        return f"Normal Guitar Playing -- Chord: {chord}, Play Tune: {tune}"

    def interpret(self, display=False):
        if not self.play_text or self.play_text.strip() == "":
            return []

        result = []
        for segment in self.play_text.split():
            i = 0
            while i < len(segment) and segment[i].isalpha():
                i += 1
            chord = segment[:i]
            tune = segment[i:]
            if display:
                self.display(chord, tune)
            result.append({"Chord": chord, "Tune": tune})
        return result

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
