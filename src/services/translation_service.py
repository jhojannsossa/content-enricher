import os
import time

from dotenv import load_dotenv
from google import genai


class TranslationService:
    """Servicio encargado de traducir contenido mediante Gemini."""

    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "No se encontró GEMINI_API_KEY en el archivo .env"
            )

        self.client = genai.Client(api_key=api_key)

    def translate(self, content: str, language: str) -> str:
        """
        Traduce el contenido al idioma indicado utilizando Gemini.
        """

        prompt = f"""
Actúa como un traductor profesional.

Traduce el siguiente documento al idioma cuyo código es: {language}

INSTRUCCIONES:

1. Traduce todo el contenido.
2. Mantén exactamente la estructura del documento.
3. Mantén los títulos y subtítulos.
4. Mantén las listas.
5. No resumas.
6. No añadas información nueva.
7. No elimines información.
8. Devuelve únicamente el texto traducido.
9. Conserva el significado original.

DOCUMENTO A TRADUCIR:

{content}
"""

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):

            try:
                print(
                    f"\nTraduciendo con Gemini "
                    f"(intento {attempt}/{max_attempts})..."
                )

                response = self.client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                if not response.text:
                    raise ValueError(
                        "Gemini no devolvió contenido traducido."
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
                            "Gemini no está disponible para la traducción "
                            f"después de {max_attempts} intentos. "
                            "Inténtalo de nuevo más tarde."
                        )

                else:
                    raise