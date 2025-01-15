/**
 * Llama a la API GPT para procesar un mensaje del usuario.
 * @param {string} userMessage - Mensaje enviado por el usuario.
 * @returns {Promise<string>} Respuesta procesada por la API o mensaje de error en caso de fallo.
 */
export async function callGPT(userMessage) {
    if (typeof userMessage !== 'string' || userMessage.trim() === '') {
        console.error('callGPT: El mensaje del usuario debe ser un string no vacío.');
        return 'El mensaje proporcionado no es válido.';
    }

    const apiUrl = 'http://127.0.0.1:5000/chat'; // URL de la API

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage }),
        });

        if (!response.ok) {
            console.error(`callGPT: Error en la respuesta de la API. Código de estado: ${response.status}`);
            throw new Error('Error en la respuesta de la API');
        }

        const data = await response.json();

        if (!data || typeof data.response !== 'string') {
            console.error('callGPT: Respuesta de la API no válida.');
            throw new Error('La respuesta de la API no contiene el formato esperado.');
        }

        return data.response;
    } catch (error) {
        console.error('callGPT: Error al comunicarse con la API:', error);
        return 'Lo siento, ocurrió un error al procesar tu solicitud. Por favor, intenta nuevamente más tarde.';
    }
}
