#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
embeddings.py

Módulo encargado de gestionar el modelo de embeddings (sentence-transformers),
y la creación/reconstrucción del índice FAISS para búsquedas semánticas.

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
"""

import numpy as np
import faiss

from config import (
    logger,
    EMBEDDINGS_AVAILABLE
)
from utils import (
    indice_global,
    file_paths
)

# Referencia al modelo de embeddings, si está disponible
# (lo cargamos en config.py o main.py si hace falta, dependiendo del diseño)
try:
    from sentence_transformers import SentenceTransformer
    embeddings_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
except ImportError:
    embeddings_model = None

# Índice FAISS que usaremos
faiss_index = None


def reconstruir_faiss():
    """
    Reconstruye la base de embeddings en FAISS usando IndexIDMap:
    - Cada archivo tiene un ID = índice correlativo.
    - Insertamos vectores para cada archivo del indice_global.
    """
    global faiss_index, file_paths

    if not EMBEDDINGS_AVAILABLE or not embeddings_model:
        logger.warning("Embeddings no disponibles: no se reconstruirá FAISS.")
        return

    # Construimos las listas de textos y sus IDs
    file_paths.clear()
    texts = []
    ids = []

    # Convierto en lista para un índice correlativo
    all_paths = list(indice_global.keys())
    for i, ruta in enumerate(all_paths):
        file_paths.append(ruta)
        texts.append(indice_global[ruta]['contenido'])
        ids.append(i)

    logger.info("Generando embeddings para todos los archivos...")
    vectors = embeddings_model.encode(texts, show_progress_bar=False)
    dimension = len(vectors[0])

    # Creamos un IndexFlatL2 y lo envolvemos en un IndexIDMap
    index_flat = faiss.IndexFlatL2(dimension)
    faiss_index = faiss.IndexIDMap(index_flat)

    # Convertimos los vectores e IDs a numpy
    vectors_np = np.array(vectors, dtype="float32")
    ids_np = np.array(ids, dtype=np.int64)

    faiss_index.add_with_ids(vectors_np, ids_np)
    logger.info("Índice FAISS reconstruido exitosamente.")


def buscar_semantico(consulta, top_k=5):
    """
    Búsqueda semántica usando FAISS + sentence-transformers.
    Retorna las rutas más relevantes.
    """
    global faiss_index, file_paths

    if not EMBEDDINGS_AVAILABLE or not embeddings_model or not faiss_index:
        return ["Embeddings no disponibles o índice no inicializado."]

    query_vector = embeddings_model.encode([consulta])
    D, I = faiss_index.search(query_vector, top_k)

    resultados = []
    for idx in I[0]:
        if 0 <= idx < len(file_paths):
            resultados.append(file_paths[idx])
    return resultados
