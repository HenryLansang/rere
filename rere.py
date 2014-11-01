import re

class RegexBase(object):
    """Base class for smart regex"""

    def match(self, string):
        return re.match(self.re_str() + '$', string)

    def match_prefix(self, string):
        return re.match(self.re_str(), string)

    def search(self, string):
        return re.search(self.re_str(), string)

    def re_str(self):
        raise NotImplementedError('subclass must implement own re_str()')

    def __add__(self, friend):
        return MultipartRegex([self, friend])

    @property
    def one_or_more(self):
        return OneOrMoreRegex(self)

    @property
    def zero_or_more(self):
        return ZeroOrMoreRegex(self)

    @property
    def zero_or_one(self):
        return ZeroOrOneRegex(self)

class RawRegex(RegexBase):
    """Match a user specified raw regex"""

    def __init__(self, pattern):
        self.pattern = pattern

    def re_str(self):
        return self.pattern

class MultipartRegex(RegexBase):
    """Container of RegexParts"""

    def __init__(self, parts):
        self.parts = parts
    
    def re_str(self):
        """Generate regex as a string"""
        multi = [part.re_str() for part in self.parts]
        return ''.join(multi)

    def __add__(self, friend):
        return MultipartRegex(self.parts + [friend])

class OneOrMoreRegex(RegexBase):

    def __init__(self, part):
        self.part = part
    
    def re_str(self):
        return '({})+'.format(self.part.re_str())

class ZeroOrMoreRegex(RegexBase):

    def __init__(self, part):
        self.part = part
    
    def re_str(self):
        return '({})*'.format(self.part.re_str())

class ZeroOrOneRegex(RegexBase):

    def __init__(self, part):
        self.part = part
    
    def re_str(self):
        return '({})?'.format(self.part.re_str())

class Exactly(RegexBase):

    def __init__(self, string):
        self.string = string

    def re_str(self):
        return re.escape(self.string)

AnyCharacter = RawRegex(r'(.|\n)')

Anything = AnyCharacter.zero_or_more