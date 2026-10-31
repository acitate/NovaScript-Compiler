
| TokenClass | Regex                  | Example |
| ---------- | ---------------------- | ------- |
| ID         | [A-Za-z_][A-Za-z0-9_]* | value   |
| LIT_INT    | [0-9]+                 | 200     |
| OPR_PLUS   | \+                     | +       |
| OPR_ASSIGN | =                      | =       |
| KW_INT     | int                    | int     |
| KW_FUNC    | func                   | func    |
| PAREN_L    | \(                     | (       |
| PAREN_R    | \)                     | )       |

Character classes:
`LETTER`: includes ASCII letters and underscore.

`DIGIT`: 0 to 9

`Whitespace`: `[ \t\r\n]+`; line comment: `//[^\r\n]*`;
block comment: `/\*([^*]|\*+[^*/])*\*+/`.