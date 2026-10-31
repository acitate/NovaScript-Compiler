from dataclasses import dataclass

from core.models.diagnostic import DiagLevel, Diagnostic
from core.models.token import Token


@dataclass
class CompilerResult:
    tokens: list[Token]
    diagnostics: list[Diagnostic]

    @property
    def success(self) -> bool:
        return not any(d.level == DiagLevel.ERROR for d in self.diagnostics)
