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
        Busca un artículo de Wikipedia relacionado con el tema.
        """

        if not topic or not topic.strip():
            raise ValueError("El tema no puede estar vacío.")

        # Primera búsqueda: búsqueda normal
        title = self._search_wikipedia(topic)

        if title:
            return title

        # Segunda búsqueda: búsqueda aproximada
        title = self._search_wikipedia(
            f"{topic}~"
        )

        if title:
            return title

        raise ValueError(
            f"No se encontró ningún artículo para: {topic}"
        )

    def _search_wikipedia(self, search_text: str) -> str | None:
        """
        Realiza una búsqueda en Wikipedia.
        """

        params = {
            "action": "query",
            "list": "search",
            "srsearch": search_text,
            "format": "json",
            "utf8": 1,
            "srlimit": 5
        }

        response = requests.get(
            self.API_URL,
            params=params,
            headers=self.HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = data.get(
            "query",
            {}
        ).get(
            "search",
            []
        )

        if not results:
            return None

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
        Extrae los primeros cinco párrafos
        con contenido.
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
        Realiza el proceso completo de búsqueda:

        1. Busca el artículo.
        2. Obtiene el HTML.
        3. Extrae los primeros cinco párrafos.
        4. Devuelve un objeto Content.
        """

        print("\nBuscando artículo en Wikipedia...")

        title = self.search_article_title(topic)

        print(f"Artículo encontrado: {title}")

        html = self.get_article_html(title)

        paragraphs = self.extract_five_paragraphs(html)

        original_content = "\n\n".join(paragraphs)

        return Content(
            title=title,
            original=original_content
        )