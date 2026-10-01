from dataclasses import dataclass


@dataclass
class Content:
    """
    Representa el contenido recopilado y procesado
    por Content Enricher.
    """

    title: str
    original: str
    enriched: str = ""
    translated: str = ""