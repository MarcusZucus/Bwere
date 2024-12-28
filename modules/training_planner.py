"""
Módulo de Entrenamientos y Rutinas.
Define planes de ejercicio (series, repeticiones, descansos) adaptados.
"""

def generate_training_plan(user_data, analysis):
    """
    Retorna un plan de entrenamiento según el análisis y el perfil del usuario.
    """
    return [
        {"exercise": "Squats", "sets": 3, "reps": 12, "rest": "60s"},
        {"exercise": "Push-ups", "sets": 3, "reps": 15, "rest": "45s"}
    ]
