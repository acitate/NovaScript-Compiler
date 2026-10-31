from dataclasses import dataclass

from core.models.diagnostic import Diagnostic
from core.models.token import Token


@dataclass
class CompilerResult:
    tokens: list[Token]
    diagnostics: list[Diagnostic]
