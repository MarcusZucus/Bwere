"""
Módulo de Seguridad y Validaciones.
Evita planes o recomendaciones peligrosas (sobreentrenamiento, déficit extremo).
"""

def validate_plans(nutrition_plan, training_plan):
    """
    Verifica si los planes son seguros y retorna True/False.
    """
    # Ejemplo básico: si el plan nutricional es muy bajo en calorías, es peligroso.
    if nutrition_plan.get("daily_calories", 0) < 1200:
        return False
    # Añade otras validaciones...
    return True
