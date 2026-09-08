from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from google import genai

app = FastAPI()

class Consulta(BaseModel):
    pregunta: str

GEMINI_KEY = os.environ.get("GEMINI_KEY")
GROQ_KEY = os.environ.get("GROQ_KEY")

@app.get("/")
def home():
    return {"status": "El servidor de la Meta-IA está activo"}

@app.post("/preguntar")
def orquestador(data: Consulta):
    pregunta = data.pregunta
    
    # Lógica de decisión: Llama 3 si pide código o programación, Gemini para el resto
    if "código" in pregunta.lower() or "programar" in pregunta.lower():
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": pregunta}]
        }
        try:
            res = requests.post(url, json=payload, headers=headers).json()
            respuesta = res['choices'][0]['message']['content']
            origen = "Llama 3.3 (Groq)"
        except Exception as e:
            respuesta = f"Error al conectar con Groq: {str(e)}"
            origen = "Error"
    else:
        try:
            client = genai.Client(api_key=GEMINI_KEY)
            res = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=pregunta
            )
            respuesta = res.text
            origen = "Gemini 2.5 (Google)"
        except Exception as e:
            respuesta = f"Error al conectar con Gemini: {str(e)}"
            origen = "Error"

    return {"respuesta": respuesta, "modelo_usado": origen}
  
