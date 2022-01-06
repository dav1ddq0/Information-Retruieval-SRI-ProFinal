from enum import Enum


class DocType(Enum):
    """TYPES OF DOCUMENTS"""
    PLAIN_TEXT = 0
    TXT= 1
    PDF = 2
    
class Doc:

    def __init__(self, name: str, path: str, type: DocType = str):
        self.name = name
        self.path = path
        self.type = type
    
    def __str__(self) -> str:
        return f"Doc: name -> {self.name} path -> {self.path} type -> {self.type}"

class Token:

    def __init__(self, word: str, freq: int) -> None:
        self.word = word
        self.freq = freq

    def __str__(self) -> str:
        return f"Token(word = {self.word}, freq = {self.freq})"

    def __ge__(self, other: 'Token'):
        return self.freq >= other.freq

    def __gt__(self, other: 'Token'):
        return self.freq > other.freq

    def __eq__(self, other: str or 'Token'):
        if isinstance(other, str):
            return self.word == other
        if isinstance(other, 'Token'):
            return self.word == other.word

