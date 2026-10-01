from deep_translator import GoogleTranslator


class TranslationService:
    """Servicio encargado de traducir contenido."""

    def translate(self, content: str, target_language: str) -> str:
        """
        Traduce el contenido al idioma seleccionado.
        """

        if not content.strip():
            raise ValueError(
                "No hay contenido para traducir."
            )

        if not target_language.strip():
            raise ValueError(
                "El idioma no puede estar vacío."
            )

        translator = GoogleTranslator(
            source="auto",
            target=target_language.lower()
        )

        return translator.translate(content)