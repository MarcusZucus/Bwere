#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py

Punto de entrada para Loid God Mode OMNISCIENTE.
Orquesta el bucle principal de interacción, carga
el historial, inicia el monitoreo, etc.

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
"""

import sys
import atexit

from config import (
    logger,
    HISTORY_FILE,
    PROJECT_REPO_PATH,
    MODO_SEGURO
)
from utils import (
    cargar_historial_persistente,
    guardar_historial_persistente,
    cargar_prompt_inicial
)
from indexing import escanear_repositorio
from validations import validar_codigo
from watchers import monitoreo_activo_inicio, monitoreo_activo_detener
from llm_integration import interpretar_peticion_natural, generar_respuesta_final
from placeholders import observabilidad_hook

# Historial global de interacciones
historial_interacciones = []


def salir_graciosamente():
    """
    Función para asegurar que, al salir, se detenga el monitoreo
    y se guarde el historial.
    """
    logger.info("Saliendo de Loid God Mode. Guardando historial y deteniendo monitoreo...")
    guardar_historial_persistente(historial_interacciones)
    monitoreo_activo_detener()
    sys.exit(0)


def main():
    global historial_interacciones

    logger.info("¡Bienvenido a Loid God Mode OMNISCIENTE (Versión Modular)!")

    # Cargamos historial previo
    historial_interacciones = cargar_historial_persistente()

    # Prompt inicial (posible desde Firebase)
    prompt_inicial = cargar_prompt_inicial()
    logger.info(f"Prompt inicial: {prompt_inicial}")

    # Indexar
    escanear_repositorio()

    # Validación inicial
    validar_codigo()

    # Iniciamos monitoreo (watchdog)
    monitoreo_activo_inicio()

    # Aseguramos limpieza al salir
    atexit.register(salir_graciosamente)

    # Bucle principal
    while True:
        try:
            prompt_usuario = input("\nTú: ")
        except (EOFError, KeyboardInterrupt):
            logger.info("Saliendo de Loid God Mode por interrupción.")
            salir_graciosamente()

        # Comandos de salida rápida
        if prompt_usuario.lower() in ["salir", "exit", "quit"]:
            salir_graciosamente()

        # Observabilidad (placeholder): recolección de métricas, logs avanzados, etc.
        observabilidad_hook(historial_interacciones)

        # Interpretar intención
        interpretacion = interpretar_peticion_natural(prompt_usuario)
        respuesta_bruta = interpretacion["respuesta_bruta"]
        funcion_detectada = interpretacion["funcion_detectada"]
        parametro = interpretacion["parametro"]

        # Manejo de ambigüedad
        if "[ACLARACION]" in respuesta_bruta:
            print("\nLoid: Tu petición es ambigua. ¿Podrías aclararla un poco más?")
            historial_interacciones.append((prompt_usuario, "Ambigüedad detectada (Loid pide aclaración)."))
            continue

        # Llamar a la función detectada si existe
        from llm_integration import llamar_funcion_interna
        funcion_resultado = None
        if funcion_detectada:
            funcion_resultado = llamar_funcion_interna(funcion_detectada, parametro)

        # Generar respuesta final
        respuesta_final = generar_respuesta_final(respuesta_bruta, funcion_resultado)
        print("\nLoid:", respuesta_final)

        # Guardar en historial
        historial_interacciones.append((prompt_usuario, respuesta_final))
        guardar_historial_persistente(historial_interacciones)


if __name__ == "__main__":
    main()
