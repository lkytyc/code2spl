import re


class RegexUtils:
    """Utility class wrapping Python's re module with general-purpose and domain-specific helpers."""

    # -------------------------------------------------------------------------
    # Core operations
    # -------------------------------------------------------------------------

    def match(self, pattern: str, text: str) -> bool:
        """Return True if pattern matches at the start of text."""
        return re.match(pattern, text) is not None

    def findall(self, pattern: str, text: str) -> list:
        """Return all non-overlapping matches of pattern in text."""
        return re.findall(pattern, text)

    def split(self, pattern: str, text: str) -> list:
        """Split text on occurrences of pattern."""
        return re.split(pattern, text)

    def sub(self, pattern: str, replacement: str, text: str) -> str:
        """Replace all matches of pattern in text with replacement."""
        return re.sub(pattern, replacement, text)

    # -------------------------------------------------------------------------
    # Pattern generators
    # -------------------------------------------------------------------------

    def generate_email_pattern(self) -> str:
        """Return a regex pattern matching email addresses in the form user@domain.tld."""
        return r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'

    def generate_phone_number_pattern(self) -> str:
        """Return a regex pattern matching US-style phone numbers in the form ###-###-####."""
        return r'\d{3}-\d{3}-\d{4}'

    def generate_split_sentences_pattern(self) -> str:
        """Return a pattern matching sentence-ending punctuation followed by 1-2 spaces and an uppercase letter."""
        return r'(?<=[.!?]) {1,2}(?=[A-Z])'

    # -------------------------------------------------------------------------
    # Higher-level methods
    # -------------------------------------------------------------------------

    def split_sentences(self, text: str) -> list:
        """Split a block of text into individual sentences using the sentence pattern."""
        pattern = self.generate_split_sentences_pattern()
        return self.split(pattern, text)

    def validate_phone_number(self, phone: str) -> bool:
        """
        Return True if phone matches a US-style phone number pattern.

        Note: uses re.match, which only anchors at the start of the string.
        A number embedded later in the string will not match.
        """
        pattern = self.generate_phone_number_pattern()
        return self.match(pattern, phone)

    def extract_email(self, text: str) -> list:
        """Find and return all email addresses in text."""
        pattern = self.generate_email_pattern()
        return self.findall(pattern, text)

import unittest

class RegexUtilsTestSub(unittest.TestCase):
    def test_sub_1(self):
        ru = RegexUtils()
        res = ru.sub(r'\b\d{3}-\d{3}-\d{4}\b', 'phone num',
                     "123-456-7890 abiguygusu 876-286-9876 kjgufwycs 987-762-9767")
        self.assertEqual(res, 'phone num abiguygusu phone num kjgufwycs phone num')

    def test_sub_2(self):
        ru = RegexUtils()
        res = ru.sub(r'\b\d{3}-\d{3}-\d{4}\b', 'phone num',
                     "1234567890 abiguygusu 8762869876 kjgufwycs 9877629767")
        self.assertEqual(res, "1234567890 abiguygusu 8762869876 kjgufwycs 9877629767")

    def test_sub_3(self):
        ru = RegexUtils()
        res = ru.sub(r'\b\d{3}-\d{3}-\d{4}\b', 'phone num',
                     "123456-7890 abiguygusu 876-286-9876 kjgufwycs 987-762-9767")
        self.assertEqual(res, '123456-7890 abiguygusu phone num kjgufwycs phone num')

    def test_sub_4(self):
        ru = RegexUtils()
        res = ru.sub(r'\b\d{3}-\d{3}-\d{4}\b', 'phone num',
                     "123-456-789a abiguygusu 876-286-9876 kjgufwycs 987-762-9767")
        self.assertEqual(res, '123-456-789a abiguygusu phone num kjgufwycs phone num')

    def test_sub_5(self):
        ru = RegexUtils()
        res = ru.sub(r'\b\d{3}-\d{3}-\d{4}\b', 'phone num',
                     "123-456-780 abiguygusu 876-286-9876 kjgufwycs 987-762-9767")
        self.assertEqual(res, '123-456-780 abiguygusu phone num kjgufwycs phone num')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
