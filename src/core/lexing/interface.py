from typing import Protocol

from core.models.result import CompilerResult


class Lexer(Protocol):

    def tokenize(self, source: str) -> CompilerResult: ...
