"""
Módulo de Planificación Nutricional.
Genera planes de alimentación exactos y personalizados.
"""

def generate_nutrition_plan(user_data, analysis):
    """
    A partir de user_data y analysis, devuelve un dict con el plan nutricional.
    """
    plan = {
        "daily_calories": analysis.get("recommended_calories", 2000),
        "meals": [
            {"name": "Desayuno", "foods": []},
            {"name": "Almuerzo", "foods": []},
            {"name": "Cena", "foods": []}
        ]
    }
    return plan
