from PIL import Image
import os

# Nombre del archivo original
original_file = "Group 200 (2) 1.png"

# Lista de tamaños y nombres de salida
sizes = [
    (72, "icon-72x72.png"),
    (96, "icon-96x96.png"),
    (128, "icon-128x128.png"),
    (144, "icon-144x144.png"),
    (152, "icon-152x152.png"),
    (192, "icon-192x192.png"),
    (384, "icon-384x384.png"),
    (512, "icon-512x512.png"),
]

# Crear una carpeta para los resultados si no existe
output_dir = "resized_icons"
os.makedirs(output_dir, exist_ok=True)

# Cargar la imagen original
try:
    original_image = Image.open(original_file)
except FileNotFoundError:
    print(f"Error: El archivo {original_file} no fue encontrado.")
    exit()

# Redimensionar y guardar cada tamaño
for size, output_name in sizes:
    resized_image = original_image.resize((size, size), Image.Resampling.LANCZOS)
    output_path = os.path.join(output_dir, output_name)
    resized_image.save(output_path, format="PNG")
    print(f"Generado: {output_path}")

print("\nTodas las imágenes han sido generadas y renombradas correctamente.")
