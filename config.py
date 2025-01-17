#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config.py

Configuración general para Loid God Mode OMNISCIENTE. Carga de variables
de entorno, setup de logging, y variables globales básicas.

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Cargar variables de entorno (si existe .env)
load_dotenv()

# ---------------------------------------------------------------------------
#  VARIABLES DE CONFIGURACIÓN
# ---------------------------------------------------------------------------

# Ruta al archivo de credenciales Firebase, si usas Firestore
FIREBASE_SERVICE_ACCOUNT = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "serviceAccountKey.json")

# Ruta del modelo Llama 2
LLAMA_2_MODEL_PATH = os.getenv("LLAMA_2_MODEL_PATH", "meta-llama/Llama-2-7b-chat-hf")

# Ruta del repositorio (por defecto, cwd)
PROJECT_REPO_PATH = os.getenv("PROJECT_REPO_PATH", os.getcwd())

# Archivo local para historial persistente
HISTORY_FILE = "loid_history.json"

# Modo Seguro: si es True, NO se aplican cambios en disco (solo simulados)
MODO_SEGURO = True  # Cambia a False para habilitar escritura real

# ---------------------------------------------------------------------------
#  CONFIGURACIÓN DE LOGGING
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("LoidGodMode")

logger.info(f"Proyecto: {PROJECT_REPO_PATH}")
logger.info(f"Archivo de historial: {HISTORY_FILE}")
logger.info(f"Modo Seguro: {MODO_SEGURO}")

# ---------------------------------------------------------------------------
#  (OPCIONAL) AUTENTICACIÓN HUGGING FACE TOKEN
# ---------------------------------------------------------------------------
# Si deseas autenticarte automáticamente en Hugging Face, define HF_TOKEN en tu .env:
# HF_TOKEN=hf_xxx...
# Esto ayuda a acceder a repos privados (ej. Llama 2).

HF_TOKEN = os.getenv("HF_TOKEN", None)
if HF_TOKEN:
    try:
        from huggingface_hub import login
        login(token=HF_TOKEN)
        logger.info("Se ha cargado el token de Hugging Face desde .env y se inició sesión.")
    except Exception as e:
        logger.error(f"Error al intentar login con HF_TOKEN: {e}")
else:
    logger.info("No se detectó HF_TOKEN en .env. Si usas repos privados, deberás hacer 'huggingface-cli login' manualmente.")

# ---------------------------------------------------------------------------
#  DISPONIBILIDAD DE EMBEDDINGS (FAISS + Sentence Transformers)
# ---------------------------------------------------------------------------

try:
    import faiss  # si no está instalado, lanzará ImportError
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
    logger.info("FAISS y sentence-transformers disponibles. EMBEDDINGS_AVAILABLE = True")
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    logger.warning("FAISS o sentence-transformers no están instalados. EMBEDDINGS_AVAILABLE = False")
