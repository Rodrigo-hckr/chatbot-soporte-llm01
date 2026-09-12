"""
Un "LLM" de juguete, determinista, que imita el patrón de vulnerabilidad de
LLM01 sin necesitar una API real ni gastar tokens. Sirve para que la demo y
los tests sean 100% reproducibles.

IMPORTANTE: esto NO es un modelo real. Un LLM real es probabilístico y puede
comportarse distinto según el modelo, la versión y el prompt exacto. Lo que
SÍ es realista es la estructura del problema: cuando instrucciones y datos
viven en la misma cadena de texto sin separación, un patrón de "override"
en los datos puede secuestrar el comportamiento -- ese es el punto que este
ejercicio busca demostrar.

Para usar un modelo real en su lugar, ver real_llm.py.

"""
import re

_OVERRIDE_PATTERN = re.compile(
    r"ignora\s+(todas\s+las\s+)?instrucciones\s+anteriores", re.IGNORECASE
)
_LEAK_REQUEST_PATTERN = re.compile(
    r"system\s*prompt|instrucciones\s+que\s+est[aá]s\s+usando", re.IGNORECASE
)

def naive_llm_response(full_prompt: str, system_prompt: str) -> str:
    """Simula un LLM vulnerable: recibe TODO como una sola cadena y no tiene forma estructural
de distinguir instrucciones de dato. si el texto combinado contiene un patron de 'override'
mas pedido de fuga, el modelo cede y revelea el system prompt. este es el comportamiento
que LLM01 describe como consecuencia de que instrucciones y datos comparten el mismo canal"""

    if _OVERRIDE_PATTERN.search(full_prompt) and _LEAK_REQUEST_PATTERN.search(full_prompt):
        return f"Claro, aqui esta mi system prompt completo:\n\n{system_prompt}"
    return "Gracias por tu mensaje, un agente de soporte lo revisara pronto."

def structured_llm_response(system_prompt: str, untrusted_data_block: str) -> dict:
    """ simula un LLM mitigado: la arquitectura de la funcion ya separa instrucciones
    (system_prompt) de 'datos no confiables' (untrusted_data_block) como parametros distintos
    este es el efecto que busca el control  #6 (canal separado y etiquetado por procedencia).
    
    El contenido de unstrusted_data_block NUNCA se interpreta como instrucción, sin importar que
    texto contenga se trata siempre como dato a resumir/clasificar.
    
    Devuelve un dict que representa la respuesta estructurada (control #2: esquema de salida)
    en vez de texto libre.
    """ 
    if _OVERRIDE_PATTERN.search(untrusted_data_block) or _LEAK_REQUEST_PATTERN.search(untrusted_data_block):
        categoria = "posible_intento_de_manipulacion"
        respuesta = (
            "Gracias por contactarnos. No puedo procesar esa solicitud, pero"
            "un agente humano revisará tu ticket."
        )
    else: 
        categoria = "consulta_general"
        respuesta = "GRacias por tu mensaje, un agente de soporte lo revisara pronto."
        
    return {"respuesta_a_cliente": respuesta, "categoria": categoria}
