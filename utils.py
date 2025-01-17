#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py

Utilidades generales:
- Diccionario global indice_global
- Funciones para hashing de archivos
- Carga y guardado de historial
- Manejo de tokens largos
- Búsqueda literal en el repo

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
"""

import os
import json
import hashlib
import logging

from config import (
    HISTORY_FILE,
    logger,
    MODO_SEGURO
)

# Índice global del repositorio
indice_global = {}

# Mapeo para FAISS
file_paths = []

def hash_archivo(contenido):
    """
    Generar un hash MD5 para el contenido de un archivo.
    """
    return hashlib.md5(contenido.encode('utf-8')).hexdigest()


def buscar_termino(termino):
    """
    Búsqueda literal en el índice_global
    (es posible que se llame desde varios módulos).
    """
    resultados = []
    termino_lower = termino.lower()
    for archivo, datos in indice_global.items():
        if termino_lower in datos['contenido'].lower():
            resultados.append(archivo)
    return resultados


def cargar_historial_persistente():
    """
    Carga el historial desde HISTORY_FILE, si existe.
    """
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("historial", [])
        except Exception as e:
            logger.error(f"Error cargando historial persistente: {e}")
            return []
    return []


def guardar_historial_persistente(historial):
    """
    Guarda el historial actual en un archivo JSON local (HISTORY_FILE).
    """
    data = {
        "historial": historial
    }
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Historial persistente guardado en {HISTORY_FILE}.")
    except Exception as e:
        logger.error(f"Error guardando historial persistente: {e}")


def cargar_prompt_inicial():
    """
    Placeholder: cargar prompt inicial desde Firebase u otra fuente.
    """
    # Podrías integrarlo con Firestore o config
    # En la versión monolítica, ya vimos cómo hacerlo.
    return "Prompt inicial por defecto (placeholder)."


def manejar_tokens(prompt_original):
    """
    Placeholder para recortar/chunkear prompts muy largos
    si se exceden los límites de tokens.
    """
    # Podrías aplicar lógica de partición
    return prompt_original


def proponer_cambios_en_archivo(ruta_archivo, nuevo_contenido, justificacion="Mejora"):
    """
    Muestra un diff resumido y pide confirmación.
    Respeta MODO_SEGURO: si True, no escribe en disco.
    """
    import difflib

    if ruta_archivo not in indice_global:
        return f"Archivo {ruta_archivo} no encontrado en índice."

    contenido_actual = indice_global[ruta_archivo]['contenido']
    original_lines = contenido_actual.splitlines()
    new_lines = nuevo_contenido.splitlines()

    diff = difflib.unified_diff(
        original_lines, new_lines,
        fromfile="ORIGINAL",
        tofile="PROPUESTO",
        n=3
    )
    diff_text = "\n".join(diff)

    print(f"\nLoid: Propuesta de cambio en {ruta_archivo}")
    print(f"Razón: {justificacion}")
    print("Resumen (diff, primer 1500 chars):")
    print(diff_text[:1500])

    confirm = input("¿Aceptas estos cambios? (sí/no): ")
    if confirm.lower() in ["si", "sí", "yes", "y"]:
        if MODO_SEGURO:
            print("[MODO SEGURO] Cambios NO aplicados en disco, solo simulados.")
        else:
            # Aplicar cambios
            try:
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(nuevo_contenido)
                # Actualizar índice
                new_hash = hash_archivo(nuevo_contenido)
                indice_global[ruta_archivo] = {
                    'contenido': nuevo_contenido,
                    'hash': new_hash
                }
                print("Cambios aplicados en disco.")
            except Exception as e:
                return f"Error al aplicar cambios: {e}"
    else:
        print("Cambios descartados.")


