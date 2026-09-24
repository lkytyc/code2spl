class NumericEntityUnescaper:
    def replace(self, input_str):
        result = []
        i = 0
        length = len(input_str)
        
        while i < length:
            if input_str[i] == '&' and i + 1 < length and input_str[i+1] == '#':
                j = i + 2
                is_hex = False
                if j < length and (input_str[j] == 'x' or input_str[j] == 'X'):
                    is_hex = True
                    j += 1
                
                start_num = j
                while j < length and input_str[j] != ';':
                    if is_hex:
                        if not self.is_hex_char(input_str[j]):
                            break
                    else:
                        if not input_str[j].isdigit():
                            break
                    j += 1
                
                if j < length and input_str[j] == ';' and j > start_num:
                    num_str = input_str[start_num:j]
                    try:
                        if is_hex:
                            code_point = int(num_str, 16)
                        else:
                            code_point = int(num_str, 10)
                        result.append(chr(code_point))
                        i = j + 1
                        continue
                    except (ValueError, OverflowError):
                        pass
                
                # Malformed or unparseable, stop processing
                break
            else:
                result.append(input_str[i])
                i += 1
        
        return ''.join(result)
    
    def is_hex_char(self, c):
        return c in '0123456789abcdefABCDEF'

import unittest

class NumericEntityUnescaperTestIsHexChar(unittest.TestCase):
    def test_is_hex_char_1(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.is_hex_char('0')
        self.assertEqual(res, True)

    def test_is_hex_char_2(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.is_hex_char('F')
        self.assertEqual(res, True)

    def test_is_hex_char_3(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.is_hex_char('G')
        self.assertEqual(res, False)

    def test_is_hex_char_4(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.is_hex_char('X')
        self.assertEqual(res, False)

    def test_is_hex_char_5(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.is_hex_char('Z')
        self.assertEqual(res, False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
