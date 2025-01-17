#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loid God Mode - El super-asistente de desarrollo definitivo.

Este script unifica:
1. Indexado incremental de tu repositorio.
2. Interacción con Llama 2 para generación y explicación de código.
3. Detección de dependencias y validación (flake8).
4. Generación automática de documentación y tests.
5. Uso de Firebase para cargar prompts iniciales y guardar historial.
6. Manejo de logs y configuración por variables de entorno.

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
"""

import os
import sys
import hashlib
import logging
import subprocess
import requests

# Manejo de variables de entorno (puedes usar .env para credenciales y configs)
# pip install python-dotenv
from dotenv import load_dotenv

# IA - LLM (Llama 2)
from transformers import AutoModelForCausalLM, AutoTokenizer

# Firebase
import firebase_admin
from firebase_admin import credentials, firestore

# ---------------------------------------------------------------------------
#  CONFIGURACIÓN INICIAL Y LOGGING
# ---------------------------------------------------------------------------

# Carga las variables de entorno desde el archivo .env (si existe)
load_dotenv()

# Ajusta el nivel de logging según necesites (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("LoidGodMode")

# Credenciales de Firebase (ruta obtenida de variable de entorno o por defecto)
FIREBASE_SERVICE_ACCOUNT = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON", "serviceAccountKey.json")

# Inicializa Firebase (manejo de excepción por si no se encuentra el archivo)
try:
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    logger.info("Firebase inicializado correctamente.")
except Exception as e:
    logger.error(f"No se pudo inicializar Firebase: {e}")
    db = None

# Modelo y tokenizer (puedes ajustar el nombre si tienes un Llama2 local)
LLAMA_2_MODEL_PATH = os.getenv("LLAMA_2_MODEL_PATH", "meta-llama/Llama-2-7b-chat-hf")
try:
    logger.info("Cargando modelo Llama 2 y tokenizer...")
    modelo = AutoModelForCausalLM.from_pretrained(LLAMA_2_MODEL_PATH)
    tokenizer = AutoTokenizer.from_pretrained(LLAMA_2_MODEL_PATH)
    logger.info("Modelo Llama 2 cargado exitosamente.")
except Exception as e:
    logger.error(f"Error cargando modelo Llama 2: {e}")
    modelo = None
    tokenizer = None

# Ruta base del repositorio (por defecto, cwd)
RUTA_REPOSITORIO = os.getenv("PROJECT_REPO_PATH", os.getcwd())
logger.info(f"Ruta del repositorio: {RUTA_REPOSITORIO}")

# Variables globales
indice_global = {}           # Índice en memoria: {ruta: {"contenido": str, "hash": str}}
historial_interacciones = [] # Historial de prompts/respuestas


# ---------------------------------------------------------------------------
#  FUNCIONES DE AYUDA
# ---------------------------------------------------------------------------

def cargar_prompt_inicial():
    """
    Cargar el prompt inicial desde Firestore.
    Se asume que existe un documento "prompt_Loid_developer" con un campo "content".
    """
    if not db:
        logger.warning("Firestore no está inicializado. Retornando prompt por defecto.")
        return "No se pudo cargar el prompt inicial de Firebase."

    try:
        doc_ref = db.collection("prompts").document("prompt_Loid_developer")
        prompt_data = doc_ref.get().to_dict()
        return prompt_data["content"]
    except Exception as e:
        logger.error(f"Error al cargar el prompt desde Firestore: {e}")
        return "Error al cargar el prompt desde Firestore."


def hash_archivo(contenido):
    """
    Generar un hash único (MD5) para el contenido de un archivo.
    Sirve para comprobar cambios sin reanalizar el archivo completo.
    """
    return hashlib.md5(contenido.encode('utf-8')).hexdigest()


# ---------------------------------------------------------------------------
#  MÓDULO DE INDEXADO Y ANÁLISIS
# ---------------------------------------------------------------------------

def escanear_repositorio():
    """
    Actualiza el índice global con los cambios en el repositorio.
    Se hace un 'hash' del contenido de cada archivo. 
    Si cambió, se actualiza en el índice. 
    """
    global indice_global
    archivos_actualizados = 0

    for root, _, files in os.walk(RUTA_REPOSITORIO):
        for archivo in files:
            ruta_completa = os.path.join(root, archivo)

            # Ignorar archivos binarios o muy grandes según convenga
            # Aquí como ejemplo, ignoramos .pyc, .git, etc.
            if any([archivo.endswith(ext) for ext in [".pyc", ".exe", ".dll"]]):
                continue
            if ".git" in ruta_completa:
                continue

            try:
                with open(ruta_completa, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                hash_actual = hash_archivo(contenido)
                # Si no existe en el índice o cambió el hash, lo actualizamos
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
    else:
        logger.info("No hay cambios en el repositorio.")


def generar_resumen_repositorio(max_caracteres_por_archivo=200):
    """
    Genera un resumen del índice global para usarlo como contexto.
    Se limita cada archivo a un máximo de caracteres para evitar exceder tokens.
    """
    resumen = "Resumen del repositorio:\n"
    for archivo, datos in indice_global.items():
        contenido_trunc = datos['contenido'][:max_caracteres_por_archivo].replace('\n', ' ')
        resumen += f"- {archivo}: {contenido_trunc}...\n"
    return resumen


def buscar_termino(termino):
    """
    Busca un término (string) en el contenido de los archivos del repositorio.
    Retorna una lista de rutas donde aparece.
    """
    resultados = []
    termino_lower = termino.lower()
    for archivo, datos in indice_global.items():
        if termino_lower in datos['contenido'].lower():
            resultados.append(archivo)
    return resultados


def detectar_dependencias():
    """
    Detecta dependencias entre archivos Python analizando sus imports.
    Retorna un diccionario {archivo: [líneas de import]}
    """
    dependencias = {}
    for archivo, datos in indice_global.items():
        if archivo.endswith('.py'):
            contenido = datos['contenido']
            imports = [
                line.strip() for line in contenido.splitlines()
                if line.startswith('import') or line.startswith('from')
            ]
            dependencias[archivo] = imports
    return dependencias


# ---------------------------------------------------------------------------
#  MÓDULO DE VALIDACIÓN
# ---------------------------------------------------------------------------

def validar_codigo():
    """
    Ejecuta un linter (flake8) para validar el código del repositorio.
    Se puede integrar con otras herramientas como pylint, mypy, bandit, etc.
    """
    try:
        logger.info("Ejecutando flake8 para validación de código...")
        resultado = subprocess.run(
            ["flake8", RUTA_REPOSITORIO],
            capture_output=True,
            text=True
        )
        if resultado.stdout:
            logger.warning("Problemas detectados:\n" + resultado.stdout)
        else:
            logger.info("¡El código está limpio! (flake8 no reportó problemas).")
    except FileNotFoundError:
        logger.error("flake8 no está instalado o no está en PATH.")
    except Exception as e:
        logger.error(f"Error al ejecutar flake8: {e}")


# ---------------------------------------------------------------------------
#  MÓDULO DE DOCUMENTACIÓN Y TESTS
# ---------------------------------------------------------------------------

def generar_documentacion():
    """
    Genera documentación básica para clases y funciones en archivos .py.
    Simplemente imprime un índice. Podría ampliarse para generar Markdown/HTML.
    """
    documentacion = {}
    for archivo, datos in indice_global.items():
        if archivo.endswith('.py'):
            contenido = datos['contenido']
            lineas = contenido.splitlines()
            clases = [line for line in lineas if line.strip().startswith("class ")]
            funciones = [line for line in lineas if line.strip().startswith("def ")]
            documentacion[archivo] = {
                "clases": clases,
                "funciones": funciones
            }

    for archivo, detalles in documentacion.items():
        print(f"\n{archivo}:\nClases:\n" + "\n".join(detalles["clases"]))
        print("Funciones:\n" + "\n".join(detalles["funciones"]))


def generar_tests():
    """
    Genera tests unitarios basados en el contenido del repositorio.
    (Por ahora solo imprime un mensaje, se podría integrar con plantillas y pytest)
    """
    logger.info("Generando tests unitarios automáticos (demostración)...")
    # Ejemplo futuro:
    # 1. Analizar cada función/clase para identificar parámetros y retornos.
    # 2. Crear un test base y guardarlo en test_nombre_modulo.py
    # 3. Ejecutar pytest automáticamente y reportar resultados.


# ---------------------------------------------------------------------------
#  MÓDULO DE INTERACCIÓN CON LLAMA 2
# ---------------------------------------------------------------------------

def interactuar_con_llama(prompt, max_length=500):
    """
    Genera respuestas o código usando el contenido del repositorio como contexto.
    Evita exceder el límite de tokens usando un resumen reducido.
    """
    if not modelo or not tokenizer:
        logger.error("El modelo Llama 2 no está inicializado. No se puede interactuar.")
        return "Error: Modelo no disponible."

    # Generar un resumen parcial (chunk) para no exceder el token limit.
    # Aquí se limita a 200 caracteres por archivo, pero puedes ajustarlo.
    contexto = generar_resumen_repositorio(max_caracteres_por_archivo=200)

    # Construir prompt completo
    prompt_completo = (
        f"{contexto}\n"
        f"---\n"
        f"Usuario: {prompt}\n"
        f"Asistente:"
    )

    # Tokenizar y generar
    entrada = tokenizer(prompt_completo, return_tensors="pt")
    salida = modelo.generate(**entrada, max_length=max_length)
    respuesta = tokenizer.decode(salida[0])
    return respuesta


# ---------------------------------------------------------------------------
#  FUNCIÓN PRINCIPAL Y BUCLE DE INTERACCIÓN
# ---------------------------------------------------------------------------

def main():
    """
    Punto de entrada principal para interactuar con Loid en modo consola.
    """
    logger.info("¡Bienvenido al Loid God Mode!")

    # Carga prompt inicial (opcional)
    prompt_inicial = cargar_prompt_inicial()
    logger.info(f"Prompt inicial: {prompt_inicial}")

    # Indexado inicial
    escanear_repositorio()

    # Ejemplo de validación automática al inicio (opcional)
    validar_codigo()

    while True:
        prompt_usuario = input("\nTú: ")
        if prompt_usuario.lower() in ["salir", "exit", "quit"]:
            logger.info("Saliendo de Loid God Mode. ¡Hasta la próxima!")
            break

        # Ejemplo: si el usuario escribe "generar documentacion"
        # llamar a la función correspondiente
        if prompt_usuario.lower() == "generar documentacion":
            generar_documentacion()
            continue

        if prompt_usuario.lower() == "generar tests":
            generar_tests()
            continue

        if prompt_usuario.lower() == "validar codigo":
            validar_codigo()
            continue

        if prompt_usuario.lower().startswith("buscar "):
            termino = prompt_usuario.split("buscar ", 1)[1]
            resultados = buscar_termino(termino)
            print(f"El término '{termino}' aparece en:")
            for res in resultados:
                print(" -", res)
            continue

        if prompt_usuario.lower().startswith("dependencias"):
            deps = detectar_dependencias()
            print("Dependencias encontradas:\n")
            for arch, imp in deps.items():
                print(f"{arch}:")
                for i in imp:
                    print(f"   {i}")
            continue

        # Interacción con Llama 2
        respuesta_llama = interactuar_con_llama(prompt_usuario)
        print("\nLoid:", respuesta_llama)
        # Se podría guardar en historial_interacciones si se desea
        historial_interacciones.append((prompt_usuario, respuesta_llama))


# ---------------------------------------------------------------------------
#  EJECUCIÓN DEL SCRIPT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Se detuvo la ejecución con Ctrl+C.")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Error fatal en Loid God Mode: {e}")
        sys.exit(1)
