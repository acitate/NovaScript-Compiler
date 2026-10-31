from dataclasses import dataclass
from enum import Enum


class TokenType(str, Enum):
    ID = "ID"

    LIT_INT = "LIT_INT"

    OPR_PLUS = "OPR_PLUS"
    OPR_ASSIGN = "OPR_ASSIGN"

    KW_INT = "KW_INT"
    KW_FUNC = "KW_FUNC"

    PAREN_L = "PAREN_L"
    PAREN_R = "PAREN_R"


@dataclass
class TokenPosition:
    line: int
    column: int
    offset: int


@dataclass
class Token:
    type: TokenType
    lexeme: str
    pos: TokenPosition
