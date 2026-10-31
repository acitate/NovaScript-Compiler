from core.lexing.interface import Lexer
from core.lexing.manual.csv_loader import DEFAULT_TABLE_PATH
from core.lexing.manual.scanner import ManualDFALexer


class Compiler:
    def __init__(self, lexer: Lexer | None = None, *, table_path=DEFAULT_TABLE_PATH):
        self._lexer, self._table_path = lexer, table_path

    def analyze_lexically(self, source):
        lexer = (
            self._lexer
            if self._lexer is not None
            else ManualDFALexer(table_path=self._table_path)
        )
        return lexer.tokenize(source)
