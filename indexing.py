#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
indexing.py

Módulo responsable de escanear el repositorio, actualizar el índice global
y (opcionalmente) reconstruir un índice FAISS para búsquedas semánticas.

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
"""

import os

from config import (
    logger,
    PROJECT_REPO_PATH,
    EMBEDDINGS_AVAILABLE
)
from utils import (
    indice_global,
    hash_archivo
)
from embeddings import (
    embeddings_model,
    reconstruir_faiss
)


def escanear_repositorio():
    """
    Actualiza el índice global con los cambios en el repositorio.
    Soporta actualización parcial para FAISS si EMBEDDINGS_AVAILABLE.
    """
    archivos_actualizados = 0

    for root, _, files in os.walk(PROJECT_REPO_PATH):
        for archivo in files:
            ruta_completa = os.path.join(root, archivo)

            # Ignorar archivos/carpetas
            if any([archivo.endswith(ext) for ext in [".pyc", ".exe", ".dll"]]):
                continue
            if ".git" in ruta_completa:
                continue

            try:
                with open(ruta_completa, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                hash_actual = hash_archivo(contenido)

                if (ruta_completa not in indice_global or
                        indice_global[ruta_completa]['hash'] != hash_actual):

                    indice_global[ruta_completa] = {
                        'contenido': contenido,
                        'hash': hash_actual
                    }
                    archivos_actualizados += 1

            except Exception as e:
                logger.debug(f"No se pudo leer {ruta_completa}: {e}")

    if archivos_actualizados > 0:
        logger.info(f"{archivos_actualizados} archivo(s) actualizado(s) en el índice.")
        if EMBEDDINGS_AVAILABLE and embeddings_model:
            logger.info("Reconstruyendo índice FAISS por cambios detectados...")
            reconstruir_faiss()
    else:
        logger.info("No hay cambios en el repositorio.")
