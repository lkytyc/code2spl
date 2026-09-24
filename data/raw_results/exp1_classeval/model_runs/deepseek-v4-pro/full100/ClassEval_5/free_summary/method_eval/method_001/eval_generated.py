class AutomaticGuitarSimulator:
    def interpret(self, text, display=False):
        if not text or not text.strip():
            return []
        result = []
        for segment in text.split():
            idx = 0
            while idx < len(segment) and segment[idx].isalpha():
                idx += 1
            chord = segment[:idx]
            tune = segment[idx:]
            item = {'Chord': chord, 'Tune': tune}
            result.append(item)
            if display:
                self.display(item)
        return result

    def display(self, item):
        return f"Normal Guitar Playing -- Chord: {item['Chord']}, Play Tune: {item['Tune']}"

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
