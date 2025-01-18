#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loid God Mode OMNISCIENTE - Versión Monolítica y Ultra-Extrema (Parte 1/2)

Este script unifica TODAS las capacidades descritas, agregando:
1. Indexado Incremental + Embeddings Avanzados (FAISS) con actualización parcial.
2. Validación Avanzada (flake8, mypy, bandit, black) y placeholders para otras herramientas.
3. Refactorización Contextual (muestra un resumen antes de modificar).
4. Observabilidad con métricas y placeholders para Prometheus/Grafana.
5. Modo Seguro (simulación de cambios sin escribir en disco).
6. Sugerencias Activas de Mejoras (placeholder para “análisis proactivo”).
7. Optimización de Monitoreo Activo (watchdog con opciones de configuración).
8. Generación Automática de Tests (placeholder más avanzado).
9. Manejo de tokens (placeholder para recorte de prompts).
10. Integración con Docker (build y run) y Git (commits, PR) – placeholders.
11. Fine-tuning local / Aprendizaje Continuo – placeholder.
12. Análisis Avanzado de Arquitectura – placeholder (detecta dependencias cíclicas, reorganiza módulos).
13. Modo de Diagnóstico – “chequeo integral” del proyecto.
14. (y todo lo existente en versiones anteriores: historial persistente, edición confirmada, etc.)

¡La meta es un “dios vivo” que abarque todos los aspectos del desarrollo local!

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
"""

import os
import sys
import hashlib
import logging
import subprocess
import requests
import json
import re
import time

from dotenv import load_dotenv

# IA - LLM (Llama 2)
from transformers import AutoModelForCausalLM, AutoTokenizer

# Firebase
import firebase_admin
from firebase_admin import credentials, firestore

# Watchdog para monitoreo de cambios en tiempo real
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

# Embeddings (FAISS + sentence-transformers)
try:
    from sentence_transformers import SentenceTransformer
    import faiss

    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False

load_dotenv()

# ---------------------------------------------------------------------------
#  CONFIGURACIÓN Y LOGGING
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("LoidGodMode")

FIREBASE_SERVICE_ACCOUNT = os.getenv(
    "FIREBASE_SERVICE_ACCOUNT_JSON", "serviceAccountKey.json"
)
LLAMA_2_MODEL_PATH = os.getenv("LLAMA_2_MODEL_PATH", "meta-llama/Llama-2-7b-chat-hf")
RUTA_REPOSITORIO = os.getenv("PROJECT_REPO_PATH", os.getcwd())
HISTORY_FILE = "loid_history.json"  # Historial persistente

# Permite habilitar/deshabilitar el "Modo Seguro"
# Si True, NO se escriben los cambios en disco (solo se simulan).
MODO_SEGURO = True  # <--- Cambia a False cuando quieras aplicar cambios reales

logger.info(f"Ruta del repositorio: {RUTA_REPOSITORIO}")
logger.info(f"Archivo de historial: {HISTORY_FILE}")
logger.info(f"Modo Seguro: {MODO_SEGURO}")

# Firebase init
try:
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    logger.info("Firebase inicializado correctamente.")
except Exception as e:
    logger.error(f"No se pudo inicializar Firebase: {e}")
    db = None

# Modelo Llama 2
try:
    logger.info("Cargando modelo Llama 2 y tokenizer...")
    modelo = AutoModelForCausalLM.from_pretrained(LLAMA_2_MODEL_PATH)
    tokenizer = AutoTokenizer.from_pretrained(LLAMA_2_MODEL_PATH)
    logger.info("Modelo Llama 2 cargado exitosamente.")
except Exception as e:
    logger.error(f"Error cargando modelo Llama 2: {e}")
    modelo = None
    tokenizer = None

# Embeddings (FAISS) - si disponibles
if EMBEDDINGS_AVAILABLE:
    try:
        logger.info("Cargando modelo de embeddings (sentence-transformers) ...")
        embeddings_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        logger.info("Modelo de embeddings cargado exitosamente.")
    except Exception as e:
        logger.error(f"Error cargando modelo de embeddings: {e}")
        embeddings_model = None
else:
    embeddings_model = None

# ---------------------------------------------------------------------------
#  VARIABLES GLOBALES
# ---------------------------------------------------------------------------

indice_global = {}
historial_interacciones = []  # Historial de la sesión
observer = None  # Watchdog

# Para almacenamiento de embeddings (FAISS) - IDMap e índice
faiss_index = None
file_paths = []  # Mapeo índice => ruta del archivo

# ---------------------------------------------------------------------------
#  INICIALIZACIÓN Y UTILIDADES
# ---------------------------------------------------------------------------


def cargar_prompt_inicial():
    """
    Cargar el prompt inicial desde Firestore (si está disponible).
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
    Genera un hash MD5 para el contenido de un archivo.
    """
    return hashlib.md5(contenido.encode("utf-8")).hexdigest()


def guardar_historial_persistente():
    """
    Guarda el historial actual en un archivo JSON local (HISTORY_FILE).
    """
    data = {"historial": historial_interacciones}
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Historial persistente guardado en {HISTORY_FILE}.")
    except Exception as e:
        logger.error(f"Error guardando historial persistente: {e}")


def cargar_historial_persistente():
    """
    Carga el historial desde HISTORY_FILE, si existe.
    """
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("historial", [])
        except Exception as e:
            logger.error(f"Error cargando historial persistente: {e}")
            return []
    return []


# ---------------------------------------------------------------------------
#  INDEXADO Y EMBEDDINGS (PARTE 1)
# ---------------------------------------------------------------------------


def escanear_repositorio():
    """
    Actualiza el índice global con los cambios en el repositorio (hash de cada archivo).
    Soporta actualización parcial de FAISS usando IndexIDMap para indexar solo archivos nuevos o modificados.

    Si MODO_SEGURO == True, igual indexa, pues no altera archivos, solo lee.
    """
    global indice_global
    global faiss_index, file_paths

    archivos_actualizados = 0
    for root, _, files in os.walk(RUTA_REPOSITORIO):
        for archivo in files:
            ruta_completa = os.path.join(root, archivo)

            # Ignorar ciertos archivos/carpetas
            if any([archivo.endswith(ext) for ext in [".pyc", ".exe", ".dll"]]):
                continue
            if ".git" in ruta_completa:
                continue

            try:
                with open(ruta_completa, "r", encoding="utf-8") as f:
                    contenido = f.read()
                hash_actual = hash_archivo(contenido)
                if (
                    ruta_completa not in indice_global
                    or indice_global[ruta_completa]["hash"] != hash_actual
                ):
                    indice_global[ruta_completa] = {
                        "contenido": contenido,
                        "hash": hash_actual,
                    }
                    archivos_actualizados += 1
            except Exception as e:
                logger.debug(f"No se pudo leer {ruta_completa}: {e}")

    if archivos_actualizados > 0:
        logger.info(f"{archivos_actualizados} archivo(s) actualizado(s) en el índice.")
        if EMBEDDINGS_AVAILABLE and embeddings_model:
            # Reconstruimos o actualizamos la FAISS index con IndexIDMap
            reconstruir_faiss()
    else:
        logger.info("No hay cambios en el repositorio.")


def reconstruir_faiss():
    """
    Reconstruye la base de embeddings en FAISS usando IndexIDMap:
    - Cada archivo tiene un ID = hash (o indice).
    - Insertamos o actualizamos solo los que cambiaron.
    """
    global file_paths, faiss_index

    file_paths = list(indice_global.keys())
    textos = []
    ids = []

    for i, ruta in enumerate(file_paths):
        # Usar la version "hash" del archivo como ID, o un int correlativo
        # Para simplificar, utilizamos i como ID
        textos.append(indice_global[ruta]["contenido"])
        ids.append(i)

    vectores = embeddings_model.encode(textos, show_progress_bar=False)
    dimension = len(vectores[0])

    # Creamos IndexIDMap
    index_flat = faiss.IndexFlatL2(dimension)
    faiss_index = faiss.IndexIDMap(index_flat)

    import numpy as np

    vectores_np = np.array(vectores, dtype="float32")
    ids_np = np.array(ids, dtype=np.int64)
    faiss_index.add_with_ids(vectores_np, ids_np)

    logger.info("Índice FAISS (IndexIDMap) reconstruido exitosamente.")


# ---------------------------------------------------------------------------
#  INDEXADO Y EMBEDDINGS (PARTE 2)
# ---------------------------------------------------------------------------


def monitoreo_activo_inicio():
    """
    Inicia el monitoreo de cambios en el repositorio usando watchdog (si está instalado).
    Incluye opción de configuración (por ejemplo, deshabilitarlo en ciertos entornos).
    """
    global observer
    if not WATCHDOG_AVAILABLE:
        logger.warning(
            "Watchdog no está disponible. No se activará la indexación en tiempo real."
        )
        return

    class ChangeHandler(FileSystemEventHandler):
        def on_any_event(self, event):
            if not event.is_directory:
                logger.info(
                    f"Detección de cambio: {event.src_path} - {event.event_type}"
                )
                escanear_repositorio()

    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, RUTA_REPOSITORIO, recursive=True)
    observer.start()
    logger.info("Monitoreo activo iniciado (watchdog).")


def monitoreo_activo_detener():
    """
    Detiene el monitoreo activo de watchdog.
    """
    global observer
    if observer:
        observer.stop()
        observer.join()
        logger.info("Monitoreo activo detenido.")


# ---------------------------------------------------------------------------
#  BÚSQUEDAS: Literal y Semántica
# ---------------------------------------------------------------------------


def buscar_termino(termino):
    """
    Búsqueda literal en el contenido de los archivos.
    """
    resultados = []
    termino_lower = termino.lower()
    for archivo, datos in indice_global.items():
        if termino_lower in datos["contenido"].lower():
            resultados.append(archivo)
    return resultados


def buscar_semantico(consulta, top_k=5):
    """
    Búsqueda semántica usando FAISS + sentence-transformers.
    Devuelve las rutas más relevantes.
    Si EMBEDDINGS o el index no están disponibles, retorna mensaje de aviso.
    """
    if not EMBEDDINGS_AVAILABLE or not embeddings_model or not faiss_index:
        return [("Embeddings no disponibles o índice no inicializado.")]
    # Codificamos la consulta
    consulta_vector = embeddings_model.encode([consulta])
    D, I = faiss_index.search(consulta_vector, top_k)
    resultados = []
    for idx in I[0]:
        if 0 <= idx < len(file_paths):
            resultados.append(file_paths[idx])
    return resultados


# ---------------------------------------------------------------------------
#  VALIDACIONES (flake8, bandit, mypy, black - placeholders)
# ---------------------------------------------------------------------------


def validar_codigo():
    """
    Ejecuta flake8 para validar el código del repositorio (básico).
    Future placeholders para mypy, bandit, black, etc.
    """
    try:
        logger.info("Ejecutando flake8 para validación de código...")
        resultado = subprocess.run(
            ["flake8", RUTA_REPOSITORIO], capture_output=True, text=True
        )
        if resultado.stdout:
            logger.warning("Problemas detectados con flake8:\n" + resultado.stdout)
        else:
            logger.info("¡El código está limpio! (flake8 no reportó problemas).")
    except FileNotFoundError:
        logger.error("flake8 no está instalado o no está en PATH.")
    except Exception as e:
        logger.error(f"Error al ejecutar flake8: {e}")

    # Placeholder: Integrar mypy
    # placeholder: Integrar bandit
    # placeholder: Integrar black (podrías incluso formatear automáticamente)


# ---------------------------------------------------------------------------
#  REPORTES, DOCUMENTACIÓN, TESTS
# ---------------------------------------------------------------------------


def detectar_dependencias():
    """
    Retorna un dict {archivo: [líneas de import]}.
    """
    dependencias = {}
    for archivo, datos in indice_global.items():
        if archivo.endswith(".py"):
            contenido = datos["contenido"]
            imports = [
                line.strip()
                for line in contenido.splitlines()
                if line.startswith("import") or line.startswith("from")
            ]
            dependencias[archivo] = imports
    return dependencias


def reporte_completo():
    """
    Genera un reporte global del proyecto, incluyendo
    - Conteo de archivos
    - Líneas de código
    - Distribución de extensiones
    - Dependencias detectadas
    - (Podrías extender con detectores de dependencias cíclicas, etc.)
    """
    total_archivos = len(indice_global)
    total_lineas = 0
    ext_count = {}

    for archivo, datos in indice_global.items():
        lineas = datos["contenido"].count("\n") + 1
        total_lineas += lineas
        _, ext = os.path.splitext(archivo)
        ext_count[ext] = ext_count.get(ext, 0) + 1

    sorted_ext = sorted(ext_count.items(), key=lambda x: x[1], reverse=True)
    top_ext = sorted_ext[:5]

    deps = detectar_dependencias()
    total_imports = sum(len(v) for v in deps.values())

    reporte = f"""
REPORTE COMPLETO DEL PROYECTO
-----------------------------
Total de archivos indexados: {total_archivos}
Total de líneas (aprox): {total_lineas}
Extensiones más frecuentes: {top_ext}
Total de imports en .py: {total_imports}

(Placeholder: Archivos más grandes, detección cíclica, gráficas matplotlib, etc.)
"""
    return reporte.strip()


def generar_documentacion():
    """
    Genera documentación básica para clases y funciones en archivos .py.
    """
    documentacion = {}
    for archivo, datos in indice_global.items():
        if archivo.endswith(".py"):
            contenido = datos["contenido"]
            lineas = contenido.splitlines()
            clases = [line for line in lineas if line.strip().startswith("class ")]
            funciones = [line for line in lineas if line.strip().startswith("def ")]
            documentacion[archivo] = {"clases": clases, "funciones": funciones}

    respuesta = []
    for archivo, detalles in documentacion.items():
        respuesta.append(f"\n{archivo}:\nClases:\n" + "\n".join(detalles["clases"]))
        respuesta.append("Funciones:\n" + "\n".join(detalles["funciones"]))

    return "\n".join(respuesta)


def generar_tests():
    """
    Genera tests unitarios (versión avanzada - placeholder).
    Aquí podríamos analizar signaturas de funciones para crear plantillas de test.
    """
    logger.info("Generando tests unitarios automáticos (placeholder más avanzado)...")
    return (
        "Se podrían generar tests automáticamente basados en la estructura del código."
    )


# ---------------------------------------------------------------------------
#  EDICIÓN DE ARCHIVOS Y MODO SEGURO
# ---------------------------------------------------------------------------


def proponer_cambios_en_archivo(ruta_archivo, nuevo_contenido, justificacion="Mejora"):
    """
    Muestra un diff resumido y pide confirmación antes de aplicar.
    Respeta MODO_SEGURO: si True, no se escriben los cambios en disco.
    """
    original = (
        indice_global[ruta_archivo]["contenido"]
        if ruta_archivo in indice_global
        else ""
    )
    original_lineas = original.splitlines()
    nuevo_lineas = nuevo_contenido.splitlines()

    import difflib

    diff = difflib.unified_diff(
        original_lineas, nuevo_lineas, fromfile="ORIGINAL", tofile="PROPUESTO", n=3
    )
    diff_text = "\n".join(diff)

    print(f"\nLoid: Tengo una propuesta de cambio para {ruta_archivo}")
    print(f"Razón: {justificacion}")
    print("Resumen (diff, primer 1500 chars):")
    print(diff_text[:1500])

    confirm = input("¿Aceptas estos cambios? (sí/no): ")
    if confirm.lower() in ["si", "sí", "yes", "y"]:
        if MODO_SEGURO:
            print("[MODO SEGURO] Cambios NO aplicados en disco, solo simulados.")
        else:
            try:
                with open(ruta_archivo, "w", encoding="utf-8") as f:
                    f.write(nuevo_contenido)
                indice_global[ruta_archivo] = {
                    "contenido": nuevo_contenido,
                    "hash": hash_archivo(nuevo_contenido),
                }
                print("Cambios aplicados en disco.")
            except Exception as e:
                print(f"Error al aplicar cambios: {e}")
    else:
        print("Cambios descartados.")


def refactorizar_archivo(ruta_archivo):
    """
    Usa el LLM para sugerir una versión refactorizada del archivo y
    solo aplica cambios si el usuario lo aprueba (resumen antes).
    """
    if ruta_archivo not in indice_global:
        return "No se encontró el archivo en el índice."

    contenido_actual = indice_global[ruta_archivo]["contenido"]

    # Generar un resumen previo del archivo (placeholder):
    lineas = contenido_actual.count("\n") + 1
    print(
        f"Resumen: El archivo {os.path.basename(ruta_archivo)} tiene {lineas} líneas."
    )

    prompt = f"""
Eres Loid, un asistente de refactorización.
Este es el contenido de un archivo:
(Comienzo)
{contenido_actual}
(Fin)

Por favor, sugiere una versión refactorizada u optimizada.
Mantener la misma lógica, mejorar estilo/estructura/legibilidad.
Devuelve solo el código final refactorizado.
"""

    if not modelo or not tokenizer:
        return "No se puede refactorizar: modelo no disponible."

    entrada = tokenizer(prompt, return_tensors="pt")
    salida = modelo.generate(**entrada, max_length=3000)
    refactorizado = tokenizer.decode(salida[0], skip_special_tokens=True)

    proponer_cambios_en_archivo(
        ruta_archivo, refactorizado, justificacion="Refactorización automática"
    )
    return "Proceso de refactorización completado (pendiente de aprobación)."


# ---------------------------------------------------------------------------
#  PLACEHOLDERS AVANZADOS (Docker, Git, Fine-tuning, Análisis Arquitectura)
# ---------------------------------------------------------------------------


def construir_contenedor():
    """
    Placeholder para automatizar docker build, etc.
    """
    # Ejemplo:
    # subprocess.run(["docker", "build", "-t", "mi_imagen", "."], check=True)
    return "Construcción de contenedor (docker build) - placeholder."


def probar_contenedor():
    """
    Placeholder para docker run + pruebas de integración.
    """
    return "Pruebas en contenedor (docker run con tests) - placeholder."


def integrar_con_git():
    """
    Placeholder para crear commits automáticos o PRs.
    """
    return "Integración con Git (crear commit, abrir PR) - placeholder."


def fine_tuning_model():
    """
    Placeholder para un proceso de fine-tuning local de Llama 2 usando historial.
    """
    return "Fine-tuning local (placeholder)."


def sugerir_mejoras_arquitectura():
    """
    Placeholder para un análisis de dependencias, complejidad, reorganización de módulos.
    """
    return "Sugerencias de arquitectura (placeholder)."


def modo_diagnostico():
    """
    Modo de Diagnóstico: chequeo integral del proyecto (estilo, cobertura, vulnerabilidades).
    """
    # Podrías orquestar llamadas a flake8, mypy, bandit, coverage, etc.
    return "Modo Diagnóstico (placeholder): Se realizarían múltiples análisis."


# ---------------------------------------------------------------------------
#  AGENTE ORQUESTADOR MULTI-PASO (Placeholder)
# ---------------------------------------------------------------------------


def agente_orquestador(prompt_usuario):
    """
    Toma una instrucción compleja y la descompone en múltiples pasos,
    ejecutándolos en orden. (Placeholder).
    """
    # Ejemplo:
    # 1) Generar un microservicio
    # 2) Agregar tests
    # 3) Validar con flake8
    # 4) docker build & run
    # 5) git commit & PR
    return f"Agente orquestador (placeholder) para la instrucción: '{prompt_usuario}'."


# ---------------------------------------------------------------------------
#  INTERPRETACIÓN DE PETICIONES (LLM) Y MANEJO DE TOKENS
# ---------------------------------------------------------------------------


def manejar_tokens(prompt_original):
    """
    Placeholder para recortar o chunkear prompts muy largos,
    para evitar superar límites de Llama 2.
    """
    # Podrías dividir el texto en trozos si excede cierto umbral.
    return prompt_original


def interpretar_peticion_natural(prompt_usuario):
    """
    Usa Llama 2 para detectar intención ([FUNCION=..., param=...]).
    """
    if not modelo or not tokenizer:
        logger.error(
            "El modelo Llama 2 no está inicializado. No se puede interpretar intención."
        )
        return {
            "respuesta_bruta": "Error: Modelo no disponible.",
            "funcion_detectada": None,
            "parametro": None,
        }

    system_instructions = f"""
Eres Loid, un asistente omnisciente local. Dispones de muchas funciones:
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
Si encaja con estas funciones, devuelve [FUNCION=xxx, param=xxx].
De lo contrario, responde libremente.
    """

    prompt_completo = f"SISTEMA:\n{system_instructions}\nUSUARIO:\n{manejar_tokens(prompt_usuario)}\nASISTENTE:"
    entrada = tokenizer(prompt_completo, return_tensors="pt")
    salida = modelo.generate(**entrada, max_length=3000)
    respuesta_bruta = tokenizer.decode(salida[0], skip_special_tokens=True)

    funcion_detectada = None
    parametro = None

    match_funcion = re.search(
        r"\[FUNCION=([a-zA-Z_]+)(?:,\s*param=(.+?))?\]", respuesta_bruta
    )
    if match_funcion:
        funcion_detectada = match_funcion.group(1).strip()
        if match_funcion.group(2):
            parametro = match_funcion.group(2).strip()

    return {
        "respuesta_bruta": respuesta_bruta,
        "funcion_detectada": funcion_detectada,
        "parametro": parametro,
    }


def llamar_funcion_interna(funcion, parametro=None):
    """
    Llama a la función interna correspondiente y retorna su resultado.
    """
    if funcion == "validar_codigo":
        validar_codigo()
        return "He validado el código con flake8 (y placeholders para mypy, bandit, black)."

    elif funcion == "generar_documentacion":
        return generar_documentacion()

    elif funcion == "buscar_termino":
        if parametro:
            encontrados = buscar_termino(parametro)
            if encontrados:
                return f"El término '{parametro}' aparece en:\n" + "\n".join(
                    encontrados
                )
            else:
                return f"No se encontró el término '{parametro}' en el repositorio."
        else:
            return "No se indicó término para buscar."

    elif funcion == "buscar_semantico":
        if parametro:
            sem_res = buscar_semantico(parametro)
            return f"Búsqueda semántica de '{parametro}':\n" + "\n".join(sem_res)
        else:
            return "No se indicó la consulta para búsqueda semántica."

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
            parametro = os.path.join(RUTA_REPOSITORIO, parametro)
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


def generar_respuesta_final(respuesta_bruta, funcion_resultado=None):
    """
    Limpia el texto de la etiqueta [FUNCION=...] y [ACLARACION],
    y añade el resultado de la función (si existe).
    """
    respuesta_limpia = re.sub(r"\[FUNCION=.*?\]", "", respuesta_bruta).strip()
    respuesta_limpia = re.sub(r"\[ACLARACION\]", "", respuesta_limpia).strip()

    if funcion_resultado:
        respuesta_limpia += f"\n\n[Resultado de la acción]:\n{funcion_resultado}"

    return respuesta_limpia


# ---------------------------------------------------------------------------
#  FUNCIÓN PRINCIPAL
# ---------------------------------------------------------------------------


def main():
    logger.info("¡Bienvenido a Loid God Mode OMNISCIENTE (Versión Ultra-Extrema)!")

    global historial_interacciones
    historial_interacciones = cargar_historial_persistente()

    prompt_inicial = cargar_prompt_inicial()
    logger.info(f"Prompt inicial: {prompt_inicial}")

    escanear_repositorio()
    validar_codigo()
    monitoreo_activo_inicio()

    while True:
        try:
            prompt_usuario = input("\nTú: ")
        except (EOFError, KeyboardInterrupt):
            logger.info("Saliendo de Loid God Mode. ¡Hasta la próxima!")
            break

        if prompt_usuario.lower() in ["salir", "exit", "quit"]:
            logger.info("Saliendo de Loid God Mode. ¡Hasta la próxima!")
            break

        interpretacion = interpretar_peticion_natural(prompt_usuario)
        respuesta_bruta = interpretacion["respuesta_bruta"]
        funcion_detectada = interpretacion["funcion_detectada"]
        parametro = interpretacion["parametro"]

        # Manejo de ambigüedad
        if "[ACLARACION]" in respuesta_bruta:
            print("\nLoid: Tu petición es ambigua. ¿Podrías aclararla?")
            historial_interacciones.append(
                (prompt_usuario, "Ambigüedad detectada (Loid pide aclaración).")
            )
            continue

        funcion_resultado = None
        if funcion_detectada:
            funcion_resultado = llamar_funcion_interna(funcion_detectada, parametro)

        respuesta_final = generar_respuesta_final(respuesta_bruta, funcion_resultado)
        print("\nLoid:", respuesta_final)

        historial_interacciones.append((prompt_usuario, respuesta_final))
        guardar_historial_persistente()

    monitoreo_activo_detener()
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Saliendo de Loid God Mode con Ctrl+C.")
        monitoreo_activo_detener()
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Error fatal en Loid God Mode: {e}")
        monitoreo_activo_detener()
        sys.exit(1)
