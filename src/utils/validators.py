def validate_topic(topic: str) -> bool:
    """Comprueba que el tema sea válido."""

    return bool(
        topic and topic.strip()
    )


def validate_language(language: str) -> bool:
    """Comprueba que el idioma sea válido."""

    return bool(
        language and language.strip()
    )


def validate_filename(filename: str) -> bool:
    """Comprueba que el nombre del archivo sea válido."""

    return bool(
        filename and filename.strip()
    )