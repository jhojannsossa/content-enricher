import requests
from bs4 import BeautifulSoup

from models.content import Content


class WikipediaService:
    """Servicio encargado de buscar y extraer información de Wikipedia."""

    API_URL = "https://es.wikipedia.org/w/api.php"

    HEADERS = {
        "User-Agent": "ContentEnricher/1.0 (Educational project)"
    }

    def search_article_title(self, topic: str) -> str:
        """
        Busca un artículo en Wikipedia relacionado con el tema.
        Devuelve el título del artículo encontrado.
        """

        if not topic or not topic.strip():
            raise ValueError("El tema no puede estar vacío.")

        params = {
            "action": "query",
            "list": "search",
            "srsearch": topic,
            "format": "json",
            "utf8": 1,
            "srlimit": 1
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

    def get_article_html(self, title: str) -> str:
        """
        Obtiene el contenido HTML de un artículo
        utilizando la API de Wikipedia.
        """

        params = {
            "action": "parse",
            "page": title,
            "prop": "text",
            "format": "json",
            "formatversion": "2"
        }

        response = requests.get(
            self.API_URL,
            params=params,
            headers=self.HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if "parse" not in data:
            raise ValueError(
                "Wikipedia no pudo devolver el contenido del artículo."
            )

        return data["parse"]["text"]

    def extract_five_paragraphs(
        self,
        html: str
    ) -> list[str]:
        """
        Utiliza BeautifulSoup para extraer
        los primeros cinco párrafos con contenido.
        """

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        paragraphs = soup.find_all("p")

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

        return valid_paragraphs

    def search(self, topic: str) -> Content:
        """
        Ejecuta el proceso completo:

        1. Busca el artículo.
        2. Obtiene su contenido.
        3. Extrae los primeros cinco párrafos.
        4. Devuelve un objeto Content.
        """

        title = self.search_article_title(topic)

        html = self.get_article_html(title)

        paragraphs = self.extract_five_paragraphs(html)

        original_content = "\n\n".join(paragraphs)

        return Content(
            title=title,
            original=original_content
        )