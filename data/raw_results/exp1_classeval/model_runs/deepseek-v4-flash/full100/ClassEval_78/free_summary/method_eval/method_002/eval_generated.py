import re

class SplitSentence:
    def __init__(self):
        self.abbreviations = {
            'mr', 'mrs', 'ms', 'dr', 'prof', 'sr', 'jr', 'st', 'vs', 'etc',
            'e.g', 'i.e', 'inc', 'ltd', 'co', 'corp', 'dept', 'assn', 'bros',
            'no', 'nos', 'fig', 'figs', 'vol', 'vols', 'pp', 'ed', 'eds',
            'trans', 'rev', 'ca', 'approx', 'appt', 'apt', 'blvd', 'ave',
            'rd', 'ct', 'ln', 'mt', 'ft', 'mgr', 'gov', 'sen', 'rep',
            'gen', 'col', 'maj', 'capt', 'lt', 'sgt', 'cpl', 'pvt',
            'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep',
            'sept', 'oct', 'nov', 'dec', 'mon', 'tue', 'tues', 'wed',
            'thu', 'thur', 'thurs', 'fri', 'sat', 'sun'
        }
        self.initials_pattern = re.compile(r'^[A-Z]\.$')
        self.sentence_split_pattern = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9])')
    
    def split_sentences(self, text):
        if not text:
            return []
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Protect abbreviations and initials from being split
        protected = []
        def protect_abbrev(match):
            protected.append(match.group(0))
            return f'\x00{len(protected)-1}\x00'
        
        # Protect common abbreviations
        abbrev_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(a) for a in self.abbreviations) + r')\.', re.IGNORECASE)
        text = abbrev_pattern.sub(protect_abbrev, text)
        
        # Protect initials like "J. K. Rowling"
        initials_pattern = re.compile(r'\b(?:[A-Z]\.\s*)+')
        text = initials_pattern.sub(protect_abbrev, text)
        
        # Split on sentence boundaries
        sentences = self.sentence_split_pattern.split(text)
        
        # Restore protected parts
        result = []
        for sent in sentences:
            def restore(match):
                idx = int(match.group(1))
                return protected[idx]
            sent = re.sub(r'\x00(\d+)\x00', restore, sent)
            sent = sent.strip()
            if sent:
                result.append(sent)
        
        return result
    
    def count_words(self, sentence):
        if not sentence:
            return 0
        # Remove punctuation and non-letter characters
        cleaned = re.sub(r'[^a-zA-Z\s]', '', sentence)
        words = cleaned.split()
        return len(words)
    
    def process_text_file(self, text):
        sentences = self.split_sentences(text)
        if not sentences:
            return 0
        max_count = 0
        for sent in sentences:
            count = self.count_words(sent)
            if count > max_count:
                max_count = count
        return max_count

import unittest

class SplitSentenceTestProcessTextFile(unittest.TestCase):
    def test_process_text_file_1(self):
        ss = SplitSentence()
        cnt = ss.process_text_file("aaa aaaa. bb bbbb bbb? cccc ccccccc cc ccc. dd ddd?")
        self.assertEqual(cnt, 4)

    def test_process_text_file_2(self):
        ss = SplitSentence()
        cnt = ss.process_text_file("Mr. Smith is a teacher. Yes.")
        self.assertEqual(cnt, 5)

    def test_process_text_file_3(self):
        ss = SplitSentence()
        cnt = ss.process_text_file("Mr. Smith is a teacher. Yes 1 2 3 4 5 6.")
        self.assertEqual(cnt, 5)

    def test_process_text_file_4(self):
        ss = SplitSentence()
        cnt = ss.process_text_file("aaa aaaa. bb bbbb bbb? cccc ccccccc cc ccc.")
        self.assertEqual(cnt, 4)

    def test_process_text_file_5(self):
        ss = SplitSentence()
        cnt = ss.process_text_file("aaa aaaa. bb bbbb bbb?")
        self.assertEqual(cnt, 3)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
