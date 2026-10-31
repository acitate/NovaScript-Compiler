import csv
from pathlib import Path

from core.lexing.manual.character_classes import CHARACTER_CLASSES
from core.lexing.manual.dfa import DFA, ERROR_ACTIONS, SKIP_ACTIONS
from core.models.token import TokenType

DEFAULT_TABLE_PATH = Path(__file__).with_name("transition_table.csv")


class TableFormatError(ValueError):
    """Invalid DFA configuration, separate from source diagnostics."""


class CSVTransitionTableLoader:
    def load(self, path=DEFAULT_TABLE_PATH, *, start_state="q0") -> DFA:
        with Path(path).open(encoding="utf-8-sig", newline="") as stream:
            rows = csv.reader(stream, strict=True)
            try:
                return self._read(rows, start_state)
            except csv.Error as exc:
                raise TableFormatError(
                    f"Invalid CSV at line {rows.line_num}: {exc}"
                ) from exc

    def _read(self, rows, start_state):
        header = [c.strip() for c in next(rows, [])]
        required = {
            "state",
            "token",
            "LETTER",
            "DIGIT",
            "PLUS",
            "ASSIGN",
            "LPAREN",
            "RPAREN",
        }
        if not required <= set(header) or set(header) - CHARACTER_CLASSES - {
            "state",
            "token",
        }:
            raise TableFormatError("Missing or unknown CSV columns.")
        if len(set(header)) != len(header):
            raise TableFormatError("Duplicate CSV column names.")
        transitions, accepting = {}, {}
        actions = {t.value for t in TokenType} | SKIP_ACTIONS | ERROR_ACTIONS
        for cells in rows:
            if not any(c.strip() for c in cells):
                continue
            if len(cells) != len(header):
                raise TableFormatError(
                    f"Wrong number of cells at line {rows.line_num}."
                )
            row = dict(zip(header, (c.strip() for c in cells)))
            state, action = row.pop("state"), row.pop("token")
            if not state or state in transitions or (action and action not in actions):
                raise TableFormatError(
                    f"Invalid/duplicate state or unknown action at line {rows.line_num}."
                )
            transitions[state] = {
                symbol: target for symbol, target in row.items() if target
            }
            if action:
                accepting[state] = action
        if start_state not in transitions or start_state in accepting or not accepting:
            raise TableFormatError(
                "Missing start/acceptance or an accepting start state."
            )
        for state, row in transitions.items():
            for symbol, target in row.items():
                if target not in transitions:
                    raise TableFormatError(
                        f"Undefined destination {target!r} at {state}/{symbol}."
                    )
        return DFA(start_state, transitions, accepting)
