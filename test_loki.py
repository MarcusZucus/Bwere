from modules.loki_conversation import start_loki_conversation

def main():
    print("Firebase initialized. Ahora puedes hablar directamente como Loki. Escribe 'salir' para terminar.\n")
    start_loki_conversation(user_id="loki")  # Asumimos que siempre eres Loki

if __name__ == "__main__":
    main()
