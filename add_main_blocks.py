import os

def add_main_block_to_scripts(target_scripts, project_path):
    """
    Añade un bloque if __name__ == "__main__": en los scripts indicados.

    Parameters:
        target_scripts (list): Lista de scripts a modificar.
        project_path (str): Ruta del proyecto donde están los scripts.
    """
    for script in target_scripts:
        script_path = os.path.join(project_path, script)
        if os.path.exists(script_path):
            try:
                with open(script_path, "r", encoding="utf-8") as file:
                    content = file.readlines()
            except UnicodeDecodeError:
                print(f"Error: No se pudo leer el archivo {script} con codificación UTF-8. Intentando con latin-1.")
                try:
                    with open(script_path, "r", encoding="latin-1") as file:
                        content = file.readlines()
                except Exception as e:
                    print(f"Error crítico al leer el archivo {script}: {e}")
                    continue

            # Verificar si ya existe el bloque `if __name__ == "__main__":`
            if any("if __name__ == \"__main__\":" in line for line in content):
                print(f"El archivo {script} ya contiene un bloque __main__.")
                continue

            # Agregar el bloque al final del archivo
            function_name = extract_main_function(content)
            main_block = "\n\nif __name__ == \"__main__\":\n"
            if function_name:
                main_block += f"    {function_name}()  # Solo se ejecutará si corres directamente {script}\n"
            else:
                main_block += f"    print(\"Ejecutando {script} directamente.\")\n"

            with open(script_path, "a", encoding="utf-8") as file:
                file.write(main_block)

            print(f"Bloque __main__ añadido a {script}.")

def extract_main_function(content):
    """
    Intenta identificar una función principal dentro del archivo.

    Parameters:
        content (list): Contenido del archivo como lista de líneas.

    Returns:
        str: Nombre de la función principal encontrada, o None si no hay.
    """
    for line in content:
        line = line.strip()
        if line.startswith("def") and "(" in line and ")" in line:
            function_name = line.split("def ")[1].split("(")[0]
            return function_name
    return None

# Definir los scripts relativos a loidmain.py
scripts = [
    "config.py",
    "main.py",
    "indexing.py",
    "embeddings.py",
    "watchers.py",
    "validations.py",
    "refactor.py",
    "llm_integration.py",
    "reports_docs_tests.py",
    "placeholders.py",
    "utils.py"
]

# Ruta del proyecto (cambiar a la ruta real de tu proyecto)
project_path = "C:/Users/marco/Desktop/werbly-project/LOID_GOD"

# Añadir el bloque __main__ a los scripts
add_main_block_to_scripts(scripts, project_path)
