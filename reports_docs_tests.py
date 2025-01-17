#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reports_docs_tests.py

Funciones para:
- reporte global (número de archivos, líneas, dependencias, etc.)
- generación de documentación (clases y funciones)
- generación de tests automáticos (placeholder)

Autor: [Tu Nombre]
Fecha: [Fecha Actual]
"""

import os
from utils import indice_global

def detectar_dependencias():
    """
    Retorna un dict {archivo: [líneas de import]}.
    """
    deps = {}
    for archivo, datos in indice_global.items():
        if archivo.endswith('.py'):
            contenido = datos['contenido']
            lines = contenido.splitlines()
            imports = [l.strip() for l in lines if l.startswith('import') or l.startswith('from')]
            deps[archivo] = imports
    return deps

def reporte_completo():
    """
    Genera un reporte global del proyecto:
    - Conteo de archivos
    - Líneas totales
    - Extensiones más frecuentes
    - Dependencias detectadas
    - Placeholder: archivos más grandes, etc.
    """
    total_archivos = len(indice_global)
    total_lineas = 0
    ext_count = {}

    for archivo, datos in indice_global.items():
        lineas = datos['contenido'].count('\n') + 1
        total_lineas += lineas
        _, ext = os.path.splitext(archivo)
        ext_count[ext] = ext_count.get(ext, 0) + 1

    top_ext = sorted(ext_count.items(), key=lambda x: x[1], reverse=True)[:5]

    # Dependencias
    all_deps = detectar_dependencias()
    total_imports = sum(len(v) for v in all_deps.values())

    rep = f"""
REPORTE COMPLETO DEL PROYECTO
-----------------------------
Total de archivos indexados: {total_archivos}
Total de líneas (aprox): {total_lineas}
Extensiones más frecuentes: {top_ext}
Total de imports en .py: {total_imports}

(Placeholder para detalles extras: archivos más grandes, detección cíclica, gráficas, etc.)
"""
    return rep.strip()


def generar_documentacion():
    """
    Genera documentación básica (clases y funciones) en los .py.
    """
    doc_out = []
    for archivo, datos in indice_global.items():
        if archivo.endswith('.py'):
            lineas = datos['contenido'].splitlines()
            clases = [l for l in lineas if l.strip().startswith("class ")]
            funcs = [l for l in lineas if l.strip().startswith("def ")]
            doc_out.append(f"\n{archivo}:\nClases:\n" + "\n".join(clases))
            doc_out.append("Funciones:\n" + "\n".join(funcs))

    return "\n".join(doc_out)


def generar_tests():
    """
    Genera tests unitarios de manera automática (placeholder).
    """
    return "Se podrían generar tests automáticamente basados en la estructura del código."
