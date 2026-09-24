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

class AutomaticGuitarSimulatorTestInterpret(unittest.TestCase):
    def test_interpret_1(self):
        context = AutomaticGuitarSimulator("C53231323")
        play_list = context.interpret()
        self.assertEqual(play_list, [{'Chord': 'C', 'Tune': '53231323'}])

    def test_interpret_2(self):
        context = AutomaticGuitarSimulator("F43231323")
        play_list = context.interpret()
        self.assertEqual(play_list, [{'Chord': 'F', 'Tune': '43231323'}])

    def test_interpret_3(self):
        context = AutomaticGuitarSimulator("Em43231323")
        play_list = context.interpret()
        self.assertEqual(play_list, [{'Chord': 'Em', 'Tune': '43231323'}])

    def test_interpret_4(self):
        context = AutomaticGuitarSimulator("G63231323")
        play_list = context.interpret()
        self.assertEqual(play_list, [{'Chord': 'G', 'Tune': '63231323'}])

    def test_interpret_5(self):
        context = AutomaticGuitarSimulator("F43231323 G63231323")
        play_list = context.interpret()
        self.assertEqual(play_list, [{'Chord': 'F', 'Tune': '43231323'}, {'Chord': 'G', 'Tune': '63231323'}])

    def test_interpret_6(self):
        context = AutomaticGuitarSimulator(" ")
        play_list = context.interpret()
        self.assertEqual(play_list, [])

    def test_interpret_7(self):
        context = AutomaticGuitarSimulator("ABC43231323 DEF63231323")
        play_list = context.interpret()
        self.assertEqual(play_list, [{'Chord': 'ABC', 'Tune': '43231323'}, {'Chord': 'DEF', 'Tune': '63231323'}])

    def test_interpret_8(self):
        context = AutomaticGuitarSimulator("C53231323")
        play_list = context.interpret(display=True)
        self.assertEqual(play_list, [{'Chord': 'C', 'Tune': '53231323'}])

    def test_interpret_9(self):
        context = AutomaticGuitarSimulator("")
        play_list = context.interpret()
        self.assertEqual(play_list, [])


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
