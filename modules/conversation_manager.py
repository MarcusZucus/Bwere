"""
Módulo de Gestión de Conversaciones de Werbly.
Registra cada turno de conversación, recupera historiales y organiza los datos para mantener el contexto.

**Propósito**:
Este módulo actúa como el núcleo para gestionar los diálogos entre el usuario y Werbly. Su función principal es registrar cada mensaje, mantener un historial cronológico y permitir que otros módulos (como `ai_core`) utilicen este historial para proporcionar respuestas contextualizadas.

**Conexión con otros módulos**:
- **Entrada de datos:** Recibe turnos de conversación generados por el usuario y respuestas de la IA.
- **Salida de historial:** Proporciona un historial estructurado al módulo `ai_core` para generar respuestas basadas en el contexto.
- **Integración con Firebase:** Utiliza `firebase_connection` para almacenar y recuperar mensajes.
- **Uso en otras capas:** Los módulos como `recommendation_engine` pueden consultar el historial para personalizar sugerencias basadas en conversaciones previas.
"""

import datetime
from modules.firebase_connection import get_firestore_client


def save_message(user_id: str, role: str, content: str):
    """
    Guarda un turno de conversación en 'usuarios/{user_id}/conversaciones'.
    Verifica que los datos no estén vacíos antes de guardarlos.

    :param user_id: Identificador único del usuario.
    :param role: Rol en la conversación ('user', 'assistant', 'system').
    :param content: Contenido del mensaje.
    """
    if not user_id or not role or not content:
        raise ValueError("Todos los campos (user_id, role, content) son obligatorios.")

    db = get_firestore_client()
    db.collection("usuarios").document(user_id)\
      .collection("conversaciones").add({
          "role": role,
          "content": content,
          "timestamp": datetime.datetime.utcnow()
      })


def get_conversation_history(user_id: str, limit: int = 50) -> list:
    """
    Recupera el historial completo o limitado de la conversación desde Firestore.
    Retorna una lista del historial en orden cronológico.

    :param user_id: Identificador único del usuario.
    :param limit: Número máximo de mensajes a recuperar (por defecto 50).
    :return: Lista de mensajes en formato [{"role": str, "content": str}].
    """
    if not user_id:
        raise ValueError("El user_id es obligatorio para recuperar el historial.")

    db = get_firestore_client()
    conversations = db.collection("usuarios").document(user_id)\
                      .collection("conversaciones").order_by("timestamp")\
                      .limit(limit).stream()

    history = [{"role": c.get("role"), "content": c.get("content")} for c in conversations]

    if not history:
        # Mensaje inicial predeterminado si no hay historial
        history.append({"role": "system", "content": "Hola, soy Werbly. ¿En qué puedo ayudarte hoy?"})

    return history


def delete_conversation_history(user_id: str):
    """
    Elimina todo el historial de conversación de un usuario desde Firestore.
    Útil para reiniciar el contexto de las conversaciones.

    :param user_id: Identificador único del usuario.
    """
    if not user_id:
        raise ValueError("El user_id es obligatorio para eliminar el historial.")

    db = get_firestore_client()
    conversations_ref = db.collection("usuarios").document(user_id).collection("conversaciones")
    batch = db.batch()

    for doc in conversations_ref.stream():
        batch.delete(doc.reference)

    batch.commit()


def summarize_conversation_history(user_id: str) -> str:
    """
    Resume el historial de conversación para proporcionar un contexto breve.
    Puede usarse por `ai_core` para cargar un resumen inicial en lugar de todo el historial.

    :param user_id: Identificador único del usuario.
    :return: Resumen de la conversación en formato texto.
    """
    history = get_conversation_history(user_id)
    messages = [f"{h['role']}: {h['content']}" for h in history]

    if not messages:
        return "El usuario aún no ha iniciado ninguna conversación con el asistente."

    # Limitar el resumen a los últimos 10 mensajes
    context = "\n".join(messages[-10:])
    return f"Resumen de conversación reciente:\n{context}"
