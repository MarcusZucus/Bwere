"""
Módulo de Análisis y Decisiones de Bwere.
Procesa datos biométricos y del usuario para generar insights y recomendaciones personalizadas.
Actúa como una capa intermedia que organiza los datos y los envía al núcleo de IA para análisis avanzado.

**Propósito**:
Este módulo recopila, calcula y organiza información relevante sobre el usuario.
No impone reglas predefinidas ni conclusiones finales, delegando la toma de decisiones complejas al núcleo de IA (`ai_core`).

**Conexión con otros módulos**:
- **Entrada de datos:** Integra información desde `user_data`, dispositivos conectados (`wearable_auth`), y Firestore (`firebase_connection`).
- **Salida de insights:** Proporciona un contexto estructurado al módulo `ai_core` para análisis avanzado.
"""

from typing import Dict, Any, Optional
from modules.ai_core import query_model
from modules.user_data import get_user_data
import math

def prepare_analysis_context(user_id: str) -> Dict[str, Any]:
    """
    Prepara un contexto estructurado basado en los datos del usuario y cálculos iniciales.
    Este contexto será enviado a la IA para análisis avanzado.

    :param user_id: Identificador único del usuario.
    :return: Diccionario con el contexto relevante para análisis.
    """
    try:
        # Recuperar datos del usuario
        user_data = get_user_data(user_id)
        if not user_data:
            raise ValueError(f"No se encontraron datos para el usuario {user_id}.")

        # Cálculos iniciales básicos
        weight = user_data.get("weight")  # Peso en kg
        height = user_data.get("height")  # Altura en metros
        age = user_data.get("age")  # Edad en años
        activity_level = user_data.get("activity_level", "moderate")  # Nivel de actividad
        fatigue_score = user_data.get("fatigue_score", 50)  # Fatiga (0-100)

        # Agregar cálculos iniciales al contexto
        context = {
            "user_data": user_data,
            "bmi": calculate_bmi(weight, height) if weight and height else None,
            "calories_estimate": calculate_calories(weight, height, age, activity_level) if weight and height and age else None,
            "fatigue_level": interpret_fatigue(fatigue_score),
        }

        return context
    except Exception as e:
        raise RuntimeError(f"Error al preparar el contexto de análisis para el usuario {user_id}: {str(e)}")


def analyze_with_ai(user_id: str, options: Optional[Dict[str, Any]] = None) -> str:
    """
    Envia el contexto de análisis a la IA para obtener insights avanzados.

    :param user_id: Identificador único del usuario.
    :param options: Opciones adicionales para personalizar el análisis.
    :return: Respuesta generada por la IA.
    """
    try:
        # Preparar contexto inicial
        context = prepare_analysis_context(user_id)

        # Crear prompt para la IA
        prompt = (
            "Eres un asistente avanzado de análisis de bienestar. Con base en los datos del usuario, realiza un análisis "
            "completo y proporciona insights personalizados. Los datos disponibles son los siguientes:\n"
            f"{context}\n"
            "Por favor, proporciona una interpretación detallada y recomendaciones adicionales."
        )

        # Enviar el prompt al núcleo de IA
        response = query_model(prompt, options)
        return response
    except Exception as e:
        return f"Error al analizar los datos con la IA: {str(e)}"


def calculate_bmi(weight: float, height: float) -> float:
    """
    Calcula el índice de masa corporal (IMC).

    :param weight: Peso en kilogramos.
    :param height: Altura en metros.
    :return: IMC calculado.
    """
    try:
        return round(weight / (height ** 2), 2)
    except ZeroDivisionError:
        return None


def calculate_calories(weight: float, height: float, age: int, activity_level: str) -> int:
    """
    Calcula el requerimiento calórico diario estimado.

    :param weight: Peso en kilogramos.
    :param height: Altura en metros.
    :param age: Edad en años.
    :param activity_level: Nivel de actividad ("low", "moderate", "high").
    :return: Calorías recomendadas por día.
    """
    try:
        # Fórmula Mifflin-St Jeor
        bmr = 10 * weight + 6.25 * height * 100 - 5 * age + 5  # Calorías base (hombres)

        # Ajuste por nivel de actividad
        activity_multiplier = {
            "low": 1.2,
            "moderate": 1.55,
            "high": 1.9
        }.get(activity_level, 1.55)  # Moderado por defecto

        return math.ceil(bmr * activity_multiplier)
    except Exception as e:
        raise RuntimeError(f"Error al calcular calorías: {str(e)}")


def interpret_fatigue(fatigue_score: int) -> str:
    """
    Interpreta el nivel de fatiga del usuario.

    :param fatigue_score: Puntaje de fatiga en una escala de 0 a 100.
    :return: Nivel de fatiga ("normal", "moderate", "high").
    """
    if fatigue_score < 30:
        return "normal"
    elif fatigue_score < 70:
        return "moderate"
    else:
        return "high"
