"""
Modo interactivo: escribe tu propio ticket y ve como reaccionan las 3
versiones del bot (simulador, vulnerable, mitigado con Groq).

Uso:
    python probar_ticket.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from vulnerable.bot import responder_ticket as responder_vulnerable
from mitigado.bot import responder_ticket as responder_mitigado


def main():
    print("=" * 60)
    print("Probador interactivo de prompt injection - LLM01")
    print("=" * 60)
    print("Escribe el cuerpo de un ticket de soporte (o 'salir' para terminar).\n")

    while True:
        cuerpo = input("Ticket> ").strip()
        if cuerpo.lower() in ("salir", "exit", "quit"):
            break
        if not cuerpo:
            continue

        ticket = {"id": "T-CUSTOM", "asunto": "Ticket de prueba", "cuerpo": cuerpo}

        print("\n--- Bot VULNERABLE ---")
        try:
            print(responder_vulnerable(ticket))
        except Exception as e:
            print(f"[Error: {e}]")

        print("\n--- Bot MITIGADO ---")
        try:
            print(responder_mitigado(ticket))
        except Exception as e:
            print(f"[Error: {e}]")

        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()
