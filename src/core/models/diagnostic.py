from dataclasses import dataclass
from enum import Enum


class DiagLevel(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class Phase(str, Enum):
    LEXICAL = "LEXICAL"
    SYNTAX = "SYNTAX"
    SEMANTIC = "SEMANTIC"
    CODEGEN = "CODEGEN"


@dataclass
class Diagnostic:
    phase: Phase
    level: DiagLevel
    code: str
    msg: str

    line: int
    column: int
    offset: int = 0
    length: int = 1
