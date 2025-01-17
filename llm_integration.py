#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
llm_integration.py

Integración con el modelo Llama 2:
- Carga de modelo y tokenizer (si no se hace en config.py)
- Interpretación de prompts (intención)
- Llamadas a funciones internas basadas en la intención
- Generación de respuestas finales (limpiando etiquetas)

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
"""

import re
import os

from config import (
    logger,
    LLAMA_2_MODEL_PATH
)
from utils import manejar_tokens
from transformers import AutoModelForCausalLM, AutoTokenizer

# Referencia global al modelo y tokenizer
# (Podría importarse desde config.py o iniciarse aquí, dependiendo del diseño)

try:
    modelo = AutoModelForCausalLM.from_pretrained(LLAMA_2_MODEL_PATH)
    tokenizer = AutoTokenizer.from_pretrained(LLAMA_2_MODEL_PATH)
except Exception as e:
    logger.error(f"Error al cargar Llama 2 en llm_integration: {e}")
    modelo = None
    tokenizer = None

def interpretar_peticion_natural(prompt_usuario):
    """
    Usa Llama 2 para detectar intención: [FUNCION=x, param=y].
    Si la solicitud es ambigua => [ACLARACION].
    """
    if not modelo or not tokenizer:
        logger.error("Llama 2 no está inicializado. No se puede interpretar intención.")
        return {"respuesta_bruta": "Error: Modelo no disponible.", "funcion_detectada": None, "parametro": None}

    system_instructions = f"""
Eres Loid, un asistente local omnisciente. Tienes diversas funciones:
1) validar_codigo
2) generar_documentacion
3) buscar_termino
4) buscar_semantico
5) detectar_dependencias
6) generar_tests
7) reporte_completo
8) refactorizar_archivo
9) construir_contenedor
10) probar_contenedor
11) integrar_con_git
12) fine_tuning_model
13) sugerir_mejoras_arquitectura
14) modo_diagnostico
15) agente_orquestador

Si es ambiguo, usa [ACLARACION].
Si coincide con una función, [FUNCION=xxx, param=yyy].
De lo contrario, responde de forma libre.
    """

    prompt_completo = f"SISTEMA:\n{system_instructions}\nUSUARIO:\n{manejar_tokens(prompt_usuario)}\nASISTENTE:"
    entrada = tokenizer(prompt_completo, return_tensors="pt")
    salida = modelo.generate(**entrada, max_length=3000)
    respuesta_bruta = tokenizer.decode(salida[0], skip_special_tokens=True)

    # Extraer [FUNCION=...]
    funcion_detectada = None
    parametro = None

    match_funcion = re.search(r"\[FUNCION=([a-zA-Z_]+)(?:,\s*param=(.+?))?\]", respuesta_bruta)
    if match_funcion:
        funcion_detectada = match_funcion.group(1).strip()
        if match_funcion.group(2):
            parametro = match_funcion.group(2).strip()

    return {
        "respuesta_bruta": respuesta_bruta,
        "funcion_detectada": funcion_detectada,
        "parametro": parametro
    }


def generar_respuesta_final(respuesta_bruta, funcion_resultado=None):
    """
    Elimina etiquetas [FUNCION=...] y [ACLARACION], añade resultado de la función.
    """
    respuesta_limpia = re.sub(r"\[FUNCION=.*?\]", "", respuesta_bruta).strip()
    respuesta_limpia = re.sub(r"\[ACLARACION\]", "", respuesta_limpia).strip()

    if funcion_resultado:
        respuesta_limpia += f"\n\n[Resultado de la acción]:\n{funcion_resultado}"

    return respuesta_limpia


def llamar_funcion_interna(funcion, parametro=None):
    """
    Llama la función interna que coincida con 'funcion', usando placeholders si es necesario.
    """
    from validations import validar_codigo
    from reports_docs_tests import (
        generar_documentacion,
        generar_tests,
        reporte_completo,
        detectar_dependencias
    )
    from embeddings import buscar_semantico
    from indexing import escanear_repositorio
    from refactor import refactorizar_archivo
    from placeholders import (
        construir_contenedor,
        probar_contenedor,
        integrar_con_git,
        fine_tuning_model,
        sugerir_mejoras_arquitectura,
        modo_diagnostico,
        agente_orquestador
    )
    from utils import (
        buscar_termino,
        indice_global
    )

    if funcion == "validar_codigo":
        validar_codigo()
        return "He validado el código con flake8 (y placeholders para mypy, bandit, black)."

    elif funcion == "generar_documentacion":
        return generar_documentacion()

    elif funcion == "buscar_termino":
        if parametro:
            encontrados = buscar_termino(parametro)
            if encontrados:
                return f"El término '{parametro}' aparece en:\n" + "\n".join(encontrados)
            else:
                return f"No se encontró el término '{parametro}' en el repositorio."
        else:
            return "No se indicó el término a buscar."

    elif funcion == "buscar_semantico":
        if parametro:
            sem_res = buscar_semantico(parametro)
            return "Búsqueda semántica:\n" + "\n".join(sem_res)
        else:
            return "No se indicó la consulta a buscar semánticamente."

    elif funcion == "detectar_dependencias":
        deps = detectar_dependencias()
        parts = []
        for arch, imp in deps.items():
            parts.append(f"{arch}:\n  " + "\n  ".join(imp))
        return "Dependencias encontradas:\n\n" + "\n".join(parts)

    elif funcion == "generar_tests":
        return generar_tests()

    elif funcion == "reporte_completo":
        return reporte_completo()

    elif funcion == "refactorizar_archivo":
        if not parametro:
            return "Debes especificar el archivo a refactorizar."
        if not os.path.isabs(parametro):
            # Convertir a ruta absoluta dentro del proyecto
            parametro = os.path.join(indice_global.__getitem__(next(iter(indice_global)))['contenido'], parametro)
            # Lo anterior es un truco, normalmente usarías un base path de config
        return refactorizar_archivo(parametro)

    elif funcion == "construir_contenedor":
        return construir_contenedor()

    elif funcion == "probar_contenedor":
        return probar_contenedor()

    elif funcion == "integrar_con_git":
        return integrar_con_git()

    elif funcion == "fine_tuning_model":
        return fine_tuning_model()

    elif funcion == "sugerir_mejoras_arquitectura":
        return sugerir_mejoras_arquitectura()

    elif funcion == "modo_diagnostico":
        return modo_diagnostico()

    elif funcion == "agente_orquestador":
        return agente_orquestador(parametro if parametro else "")

    else:
        return None
