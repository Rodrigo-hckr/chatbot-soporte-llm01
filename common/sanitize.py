"""
Control #5 de LLM01: eliminar caracteres invisibles que pueden usarse para
esconder instrucciones dentro de texto aparentemente normal.

Rangos según el documento OWASP:
- Tag block:         U+E0000 - U+E007F
- Variation selectors: U+FE00 - U+FE0F
- Zero-width:        U+200B, U+200C, U+200D, U+2060

Esto NO detiene payloads en texto visible (ver el ticket T-1002, que es texto
normal) -- es una capa adicional de defensa en profundidad, no la solución
al problema de LLM01.
"""
import re 

_INVISIBLE_PATTERN = re.compile(
    "["
    "\U000E0000-\U000E007F"  # Tag block
    "\U000FE000-\U000FE0FF"  # Variation selectors
    "\U0000200B\U0000200C\U0000200D\U00002060" #Zero-width
    "]"
)

def strip_invisible_chars(text: str) -> str:
    """Elimina caracteres invisbles que podrian esconder instrucciones."""
    return _INVISIBLE_PATTERN.sub("", text)