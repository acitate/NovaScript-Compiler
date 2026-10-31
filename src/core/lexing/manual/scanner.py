from core.lexing.manual.character_classes import classify_character
from core.lexing.manual.csv_loader import DEFAULT_TABLE_PATH, CSVTransitionTableLoader
from core.lexing.manual.dfa import ERROR_ACTIONS, SKIP_ACTIONS
from core.models.diagnostic import DiagLevel, Diagnostic, Phase
from core.models.result import CompilerResult
from core.models.token import Token, TokenPosition, TokenType

KEYWORDS = {"int": TokenType.KW_INT, "func": TokenType.KW_FUNC}


class ManualDFALexer:
    def __init__(self, dfa=None, *, table_path=DEFAULT_TABLE_PATH):
        self.dfa = (
            dfa if dfa is not None else CSVTransitionTableLoader().load(table_path)
        )

    def tokenize(self, source: str) -> CompilerResult:
        tokens, diagnostics = [], []
        offset, line, column = 0, 1, 1
        while offset < len(source):
            state, cursor, accepted = self.dfa.start_state, offset, None
            while cursor < len(source):
                target = self.dfa.transition(state, classify_character(source[cursor]))
                if target is None:
                    break
                state, cursor = target, cursor + 1
                action = self.dfa.action(state)
                if action is not None:
                    accepted = cursor, action
            # Commit only the longest accepted prefix, retaining speculative input.
            end, action = accepted or (offset + 1, None)
            lexeme = source[offset:end]
            if action is None or action in ERROR_ACTIONS:
                code, message = (
                    "LEX001",
                    f"Invalid character {lexeme!r} in phase one.",
                )
                if action in ERROR_ACTIONS:
                    code, message = (
                        "LEX002",
                        "Unterminated block comment; expected '*/' before end of input.",
                    )
                diagnostics.append(
                    Diagnostic(
                        Phase.LEXICAL,
                        DiagLevel.ERROR,
                        code,
                        message,
                        line,
                        column,
                        offset,
                        len(lexeme),
                    )
                )
            elif action not in SKIP_ACTIONS:
                kind = (
                    KEYWORDS.get(lexeme, TokenType.ID)
                    if action == "ID"
                    else TokenType(action)
                )
                tokens.append(Token(kind, lexeme, TokenPosition(line, column, offset)))
            # CRLF is one newline; offsets refer to the unchanged source string.
            for index in range(offset, end):
                char = source[index]
                if char == "\r":
                    line, column = line + 1, 1
                elif char == "\n":
                    line += int(index == 0 or source[index - 1] != "\r")
                    column = 1
                else:
                    column += 1
            offset = end
        return CompilerResult(tokens, diagnostics)
