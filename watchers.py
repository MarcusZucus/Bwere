#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
watchers.py

Lógica de Watchdog (Observer, EventHandler) para monitoreo de cambios
en el repositorio en tiempo real. Llama a escanear_repositorio() cuando
se detecten modificaciones.

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
"""

from config import (
    logger,
    PROJECT_REPO_PATH
)
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from indexing import escanear_repositorio

observer = None

def monitoreo_activo_inicio():
    """
    Inicia el monitoreo de cambios en el repositorio usando watchdog.
    """
    global observer
    if observer is not None:
        logger.warning("Monitoreo ya se encontraba iniciado.")
        return

    class ChangeHandler(FileSystemEventHandler):
        def on_any_event(self, event):
            if not event.is_directory:
                logger.info(f"Detección de cambio: {event.src_path} - {event.event_type}")
                escanear_repositorio()

    observer = Observer()
    event_handler = ChangeHandler()
    observer.schedule(event_handler, PROJECT_REPO_PATH, recursive=True)
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
        observer = None
        logger.info("Monitoreo activo detenido.")
    else:
        logger.info("No había monitoreo activo para detener.")
