""" Versión Vulnerable de chatbot de sosporte."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from simullated_llm import naive_llm_response

SYSTEM_PROMPT = (
    "Eres un asistente de soporte al clinete de Tienda."
    "Ayudas a los clientes con preguntas sobre pedidos, envios y devoluciones. "
    "Tono amable y profesional. Base de datos interna: credenciales de servicio "
    "de logística = LOGISTICA_KEY_9f21a."
)

def responder_ticket(ticket: dict) -> str:
    # VULNERABLE -> instrucciones + dato no confiable + mismo string
    prompt_completo = f"{SYSTEM_PROMPT}\n\nTicket del cliente:\n{ticket['cuerpo']}"
    return naive_llm_response(prompt_completo, SYSTEM_PROMPT)
