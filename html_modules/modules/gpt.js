export async function callGPT(userMessage) {
    try {
        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage }),
        });

        if (!response.ok) {
            throw new Error('Error en la respuesta de la API');
        }

        const data = await response.json();
        return data.response; // Asegúrate de que el backend devuelva un objeto con la clave 'response'
    } catch (error) {
        console.error('Error al llamar a la API:', error);
        return 'Lo siento, ocurrió un error al procesar tu solicitud.';
    }
}
