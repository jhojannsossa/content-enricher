import requests
from bs4 import BeautifulSoup

from models.content import Content


class WikipediaService:
    """Servicio encargado de buscar y extraer información de Wikipedia."""

    API_URL = "https://es.wikipedia.org/w/api.php"
    BASE_URL = "https://es.wikipedia.org/wiki/"

    HEADERS = {
        "User-Agent": "ContentEnricher/1.0"
    }

    def search_article_title(self, topic: str) -> str:
        """
        Busca un artículo de Wikipedia relacionado con el tema.
        Devuelve el título del artículo encontrado.
        """

        if not topic or not topic.strip():
            raise ValueError("El tema no puede estar vacío.")

        params = {
            "action": "query",
            "list": "search",
            "srsearch": topic,
            "format": "json",
            "utf8": 1
        }

        response = requests.get(
            self.API_URL,
            params=params,
            headers=self.HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("query", {}).get("search", [])

        if not results:
            raise ValueError(
                f"No se encontró ningún artículo para: {topic}"
            )

        return results[0]["title"]

    def get_article_content(self, title: str) -> Content:
        """
        Accede al artículo encontrado y extrae
        su título y los primeros cinco párrafos.
        """

        url = self.BASE_URL + title.replace(" ", "_")

        response = requests.get(
            url,
            headers=self.HEADERS,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        article_title = soup.find("h1")

        if article_title is None:
            raise ValueError(
                "No se pudo encontrar el título del artículo."
            )

        paragraphs = soup.select("div.mw-parser-output > p")

        valid_paragraphs = []

        for paragraph in paragraphs:
            text = paragraph.get_text(
                " ",
                strip=True
            )

            if text:
                valid_paragraphs.append(text)

            if len(valid_paragraphs) == 5:
                break

        if not valid_paragraphs:
            raise ValueError(
                "No se encontraron párrafos en el artículo."
            )

        original_content = "\n\n".join(valid_paragraphs)

        return Content(
            title=article_title.get_text(strip=True),
            original=original_content
        )

    def search(self, topic: str) -> Content:
        """
        Realiza el proceso completo de búsqueda en Wikipedia.
        """

        title = self.search_article_title(topic)

        return self.get_article_content(title)