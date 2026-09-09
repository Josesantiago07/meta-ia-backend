
import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Inicializa el cliente usando la clave de Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/preguntar', methods=['POST'])
def preguntar():
    try:
        data = request.get_json()
        pregunta_usuario = data.get('pregunta', '')

        if not pregunta_usuario:
            return jsonify({'respuesta': 'Por favor escribe una pregunta.'}), 400

        # Petición al modelo de código abierto Mixtral / Mistral
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente de Inteligencia Artificial útil, amigable y conciso."
                },
                {
                    "role": "user",
                    "content": pregunta_usuario,
                }
            ],
            model="mixtral-8x7b-32768",  # Modelo 100% libre de Gemini y Meta
        )

        respuesta_ia = chat_completion.choices[0].message.content
        return jsonify({'respuesta': respuesta_ia})

    except Exception as e:
        return jsonify({'respuesta': f"Error en el servidor: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
