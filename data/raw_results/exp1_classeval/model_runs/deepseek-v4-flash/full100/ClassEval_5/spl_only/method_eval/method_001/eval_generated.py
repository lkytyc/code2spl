class AutomaticGuitarSimulator:
    def __init__(self, text):
        self.play_text = text

    def interpret(self, display=False):
        if not self.play_text.strip():
            return []

        play_list = []
        play_segs = self.play_text.split(' ')

        for play_seg in play_segs:
            pos = 0
            for ele in play_seg:
                if not ele.isalpha():
                    break
                pos += 1

            play_chord = play_seg[0:pos]
            play_value = play_seg[pos:]

            play_list.append({"Chord": play_chord, "Tune": play_value})

            if display:
                self.display(play_chord, play_value)

        return play_list

    def display(self, key, value):
        formatted_message = 'Normal Guitar Playing -- Chord: %s, Play Tune: %s' % (str(key), str(value))
        return formatted_message

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
