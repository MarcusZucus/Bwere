"""
Módulo de Análisis y Decisiones de Werbly.
Procesa datos biométricos y del usuario para generar insights y recomendaciones personalizadas.
Integra datos de otros módulos (como `user_data` y `ai_core`) para enriquecer las conclusiones.

**Propósito**:
Este módulo actúa como una capa intermedia entre los datos brutos del usuario y los módulos que generan recomendaciones (por ejemplo, `nutrition_planner` y `training_planner`). Su función principal es analizar los datos disponibles y preparar resúmenes que puedan ser utilizados por otros módulos o enviados a la IA para análisis avanzado.

**Conexión con otros módulos**:
- **Entrada de datos:** Recibe información del módulo `user_data` y de dispositivos conectados a través de `api_integration_manager`.
- **Salida de insights:** Proporciona conclusiones procesadas a módulos como `nutrition_planner`, `training_planner`, y `recommendation_engine`.
- **Interacción con la IA:** Puede delegar tareas más complejas al módulo `ai_core` para análisis adicionales.
"""

from typing import Dict, Any
import math

def analyze_user_data(user_data: dict) -> Dict[str, Any]:
    """
    Analiza datos del usuario y retorna un diccionario con conclusiones.

    :param user_data: Información sobre el usuario, como peso, altura, edad, actividad física, etc.
    :return: Diccionario con insights personalizados para el usuario.
    """
    # Recuperar datos básicos
    weight = user_data.get("weight")  # Peso en kg
    height = user_data.get("height")  # Altura en metros
    age = user_data.get("age")  # Edad en años
    activity_level = user_data.get("activity_level", "moderate")  # Nivel de actividad
    fatigue_score = user_data.get("fatigue_score", 50)  # Fatiga (0-100)

    # Cálculos básicos
    bmi = calculate_bmi(weight, height) if weight and height else None
    recommended_calories = calculate_calories(weight, height, age, activity_level) if weight and height and age else None
    fatigue_level = interpret_fatigue(fatigue_score)

    # Necesidades nutricionales adicionales
    needs_more_protein = bmi and bmi < 18.5  # Personas con bajo peso necesitan más proteínas.

    return {
        "bmi": bmi,
        "recommended_calories": recommended_calories,
        "fatigue_level": fatigue_level,
        "needs_more_protein": needs_more_protein,
        "summary": generate_summary(bmi, recommended_calories, fatigue_level)
    }


def calculate_bmi(weight: float, height: float) -> float:
    """
    Calcula el índice de masa corporal (IMC).

    :param weight: Peso en kilogramos.
    :param height: Altura en metros.
    :return: IMC calculado.
    """
    return round(weight / (height ** 2), 2)


def calculate_calories(weight: float, height: float, age: int, activity_level: str) -> int:
    """
    Calcula el requerimiento calórico diario estimado.

    :param weight: Peso en kilogramos.
    :param height: Altura en metros.
    :param age: Edad en años.
    :param activity_level: Nivel de actividad ("low", "moderate", "high").
    :return: Calorías recomendadas por día.
    """
    # Fórmula Mifflin-St Jeor
    bmr = 10 * weight + 6.25 * height * 100 - 5 * age + 5  # Calorías base (para hombres)
    
    # Ajuste por nivel de actividad
    activity_multiplier = {
        "low": 1.2,
        "moderate": 1.55,
        "high": 1.9
    }.get(activity_level, 1.55)  # Moderado por defecto

    return math.ceil(bmr * activity_multiplier)


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


def generate_summary(bmi: float, calories: int, fatigue: str) -> str:
    """
    Genera un resumen interpretativo de los datos analizados.

    :param bmi: Índice de masa corporal.
    :param calories: Calorías recomendadas.
    :param fatigue: Nivel de fatiga.
    :return: Resumen textual.
    """
    return (
        f"Tu IMC es {bmi}, lo que indica un {'peso saludable' if 18.5 <= bmi <= 24.9 else 'peso no óptimo'}. "
        f"Se recomienda consumir aproximadamente {calories} calorías por día. "
        f"Tu nivel de fatiga actual es {fatigue}."
    )
