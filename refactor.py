#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refactor.py

Lógica de refactorización y diffs con el LLM (Llama 2),
con confirmación del usuario antes de aplicar cambios.
Respeta el modo seguro definido en config.py.

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
"""

import os

from config import (
    logger,
    MODO_SEGURO
)
from utils import (
    indice_global,
    hash_archivo,
    proponer_cambios_en_archivo
)
from llm_integration import (
    modelo,
    tokenizer
)


def refactorizar_archivo(ruta_archivo):
    """
    Usa el LLM para sugerir una versión refactorizada del archivo y 
    solo aplica cambios si el usuario lo aprueba (proponiendo un diff).
    """
    if ruta_archivo not in indice_global:
        return "No se encontró el archivo en el índice."

    contenido_actual = indice_global[ruta_archivo]['contenido']

    # Mostramos un resumen simple, p.ej. número de líneas:
    lineas = contenido_actual.count('\n') + 1
    logger.info(f"Refactor: El archivo {os.path.basename(ruta_archivo)} tiene {lineas} líneas.")

    # Prompt para el LLM
    prompt = f"""
Eres Loid, un asistente de refactorización.
Este es el contenido del archivo a refactorizar:
(Comienzo)
{contenido_actual}
(Fin)

Por favor, sugiere una versión refactorizada:
- Mantener la misma lógica
- Mejorar estilo, estructura y legibilidad
- Devuelve solo el código final refactorizado
"""

    if not modelo or not tokenizer:
        return "No se puede refactorizar: modelo no disponible."

    # Generamos la respuesta del LLM
    entrada = tokenizer(prompt, return_tensors="pt")
    salida = modelo.generate(**entrada, max_length=3000)
    refactorizado = tokenizer.decode(salida[0], skip_special_tokens=True)

    # Proponemos cambios
    resultado = proponer_cambios_en_archivo(ruta_archivo, refactorizado, justificacion="Refactorización automática")
    return resultado or "Proceso de refactorización finalizado (pendiente de aprobación)."
