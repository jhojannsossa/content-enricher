import os
import time

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
        Enriquece y organiza el contenido mediante Gemini.
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

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):

            try:
                print(
                    f"\nIntentando conectar con Gemini "
                    f"(intento {attempt}/{max_attempts})..."
                )

                response = self.client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                if not response.text:
                    raise ValueError(
                        "Gemini no devolvió contenido."
                    )

                return response.text

            except Exception as error:

                error_message = str(error)

                if "503" in error_message or "UNAVAILABLE" in error_message:

                    if attempt < max_attempts:
                        print(
                            "\nGemini está temporalmente saturado."
                        )
                        print(
                            "Esperando 5 segundos antes de volver a intentarlo..."
                        )

                        time.sleep(5)

                    else:
                        raise Exception(
                            "Gemini no está disponible después de "
                            f"{max_attempts} intentos. "
                            "Inténtalo de nuevo más tarde."
                        )

                else:
                    raise