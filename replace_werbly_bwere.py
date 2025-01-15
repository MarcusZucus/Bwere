import os
import re

def replace_in_file(file_path, old_word, new_word):
    """Reemplaza todas las ocurrencias de old_word por new_word en un archivo."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Reemplazar usando una búsqueda insensible a mayúsculas/minúsculas
        pattern = re.compile(re.escape(old_word), re.IGNORECASE)
        if pattern.search(content):
            content = pattern.sub(new_word, content)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Reemplazo completado en: {file_path}")
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")

def replace_in_repo(repo_path, old_word, new_word):
    """Recorre recursivamente todos los archivos en un repositorio para reemplazar palabras."""
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Analizando archivo: {file_path}")  # Log para verificar archivos
            # Procesar solo archivos de texto o código
            if file.endswith(('.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.yaml', '.yml', '.java', '.php', '.xml')):
                replace_in_file(file_path, old_word, new_word)

# Configuración del script
repo_path = "C:\\Users\\marco\\Desktop\\Bwere-project"  # Cambia esto al directorio de tu repositorio
old_word = "Bwere"
new_word = "Bwere"

# Ejecutar reemplazo
replace_in_repo(repo_path, old_word, new_word)
