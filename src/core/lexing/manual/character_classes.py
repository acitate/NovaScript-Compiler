import string

CHARACTER_CLASSES = frozenset("LETTER DIGIT PLUS ASSIGN LPAREN RPAREN SPACE NEWLINE SLASH STAR OTHER".split())
_CLASSES = {
    **dict.fromkeys(string.ascii_letters + "_", "LETTER"),
    **dict.fromkeys(string.digits, "DIGIT"),
    **dict.fromkeys(" \t\v\f", "SPACE"), **dict.fromkeys("\r\n", "NEWLINE"),
    "+": "PLUS", "=": "ASSIGN", "(": "LPAREN", ")": "RPAREN", "/": "SLASH", "*": "STAR",
}

def classify_character(char: str) -> str:
    print(_CLASSES)
    return _CLASSES.get(char, "OTHER")
