import os
import pandas as pd

def process_opensim_data(input_dir, output_dir, supported_formats=[".sto", ".mot"]):
    """
    Procesa archivos de OpenSim y los convierte a formato CSV.
    """
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if any(file.endswith(ext) for ext in supported_formats):
            file_path = os.path.join(input_dir, file)
            try:
                # Leer el archivo como tabla
                data = pd.read_csv(file_path, delimiter="\t", comment=";", skip_blank_lines=True)
                output_file = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.csv")
                data.to_csv(output_file, index=False)
                print(f"Procesado: {file} -> {output_file}")
            except Exception as e:
                print(f"Error procesando {file}: {e}")
