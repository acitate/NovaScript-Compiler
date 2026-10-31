from dataclasses import dataclass

SKIP_ACTIONS = frozenset({"SKIP_WHITESPACE", "SKIP_COMMENT"})
ERROR_ACTIONS = frozenset({"ERROR_UNTERMINATED_COMMENT"})


@dataclass(frozen=True)
class DFA:
    start_state: str
    transitions: dict[str, dict[str, str]]
    accepting: dict[str, str]

    def transition(self, state, char_class):
        return self.transitions[state].get(char_class)

    def action(self, state):
        return self.accepting.get(state)
