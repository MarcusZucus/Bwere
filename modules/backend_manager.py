'''
Módulo de Manejo de Backends (backend_manager).
Gestiona y registra backends personalizados, permitiendo agregar o eliminar módulos de IA adicionales 
de forma dinámica.

**Propósito**:
- Centraliza la gestión de backends personalizados.
- Proporciona funciones para registrar, eliminar y verificar el estado de los backends.

**Conexión con otros módulos**:
- Integrado con `ai_core` para centralizar el acceso a los modelos de IA.
- Permite pruebas de integración con los backends configurados.
'''

import logging
import requests

# Configuración del sistema de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BackendManager:
    """
    Clase para gestionar backends personalizados.
    """

    def __init__(self):
        self.custom_backends = {}

    def register_backend(self, name: str, handler: callable):
        """
        Registra un nuevo backend personalizado.

        :param name: Nombre del backend.
        :param handler: Función que maneja las consultas para este backend.
        """
        if name in self.custom_backends:
            logging.warning(f"El backend '{name}' ya está registrado. Sobrescribiendo...")
        self.custom_backends[name] = handler
        logging.info(f"Backend personalizado registrado: {name}")

    def remove_backend(self, name: str):
        """
        Elimina un backend personalizado registrado.

        :param name: Nombre del backend a eliminar.
        """
        if name in self.custom_backends:
            del self.custom_backends[name]
            logging.info(f"Backend personalizado eliminado: {name}")
        else:
            logging.warning(f"Intento de eliminar un backend no registrado: {name}")

    def list_backends(self):
        """
        Lista los backends personalizados registrados.

        :return: Diccionario con los backends registrados.
        """
        logging.info(f"Backends registrados: {list(self.custom_backends.keys())}")
        return self.custom_backends

    def test_backend(self, name: str, test_function: callable = None) -> bool:
        """
        Prueba la disponibilidad de un backend personalizado.

        :param name: Nombre del backend a probar.
        :param test_function: Función personalizada para probar el backend.
        :return: True si el backend está disponible, False en caso contrario.
        """
        if name not in self.custom_backends:
            logging.error(f"El backend '{name}' no está registrado.")
            return False

        try:
            if test_function:
                result = test_function()
                logging.info(f"Prueba del backend '{name}' resultó en: {result}")
                return result
            else:
                # Si no se proporciona una función de prueba, asumimos que el backend está disponible.
                logging.info(f"Prueba predeterminada para el backend '{name}' fue exitosa.")
                return True
        except Exception as e:
            logging.error(f"Error al probar el backend '{name}': {str(e)}")
            return False

    def test_all_backends(self) -> dict:
        """
        Prueba la disponibilidad de todos los backends registrados.

        :return: Diccionario con el estado de cada backend (True si está disponible, False si no lo está).
        """
        results = {}
        for name, handler in self.custom_backends.items():
            try:
                results[name] = self.test_backend(name)
            except Exception as e:
                logging.error(f"Error al probar el backend '{name}': {str(e)}")
                results[name] = False
        logging.info(f"Resultados de las pruebas de backends: {results}")
        return results

    def query_backend(self, name: str, prompt: str, options: dict = None) -> str:
        """
        Envía una consulta a un backend personalizado.

        :param name: Nombre del backend.
        :param prompt: Prompt que se enviará al backend.
        :param options: Opciones adicionales para la consulta.
        :return: Respuesta generada por el backend.
        """
        if name not in self.custom_backends:
            logging.error(f"El backend '{name}' no está registrado.")
            return "Error: Backend no registrado."

        try:
            handler = self.custom_backends[name]
            response = handler(prompt, options)
            logging.info(f"Respuesta del backend '{name}': {response}")
            return response
        except Exception as e:
            logging.error(f"Error al consultar el backend '{name}': {str(e)}")
            return f"Error al consultar el backend: {str(e)}"

# Ejemplo de uso del BackendManager
if __name__ == "__main__":
    manager = BackendManager()

    # Registrar un backend de ejemplo
    def example_handler(prompt, options):
        return f"Ejemplo de respuesta para el prompt: {prompt}"

    manager.register_backend("example", example_handler)

    # Consultar el backend
    print(manager.query_backend("example", "Este es un prompt de prueba"))

    # Listar backends
    print(manager.list_backends())

    # Probar todos los backends
    print(manager.test_all_backends())

    # Eliminar un backend
    manager.remove_backend("example")
    print(manager.list_backends())
