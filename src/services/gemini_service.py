import os

from dotenv import load_dotenv
from google import genai


class GeminiService:
    """Servicio encargado de enriquecer contenido mediante Gemini."""

    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "No se encontró GEMINI_API_KEY en el archivo .env"
            )

        self.client = genai.Client(api_key=api_key)

    def enrich(self, title: str, content: str) -> str:
        """
        Enriquece y organiza el contenido para convertirlo
        en material de estudio.
        """

        prompt = f"""
Actúa como un asistente especializado en crear
material educativo.

Tema:
{title}

Contenido original:
{content}

Transforma este contenido en un documento de estudio
claro, estructurado y útil.

Debes:

1. Crear una breve introducción.
2. Explicar las ideas principales.
3. Organizar la información con títulos y subtítulos.
4. Utilizar listas cuando sea apropiado.
5. Mantener información relevante.
6. No inventar datos que no estén presentes en el contenido.
7. Terminar con un breve resumen para repasar.

Devuelve únicamente el documento de estudio.
"""

        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        if not response.text:
            raise ValueError(
                "Gemini no devolvió contenido."
            )

        return response.text