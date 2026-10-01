import requests
from bs4 import BeautifulSoup


class WikipediaService:
    """Servicio encargado de obtener información desde Wikipedia."""

    BASE_URL = "https://es.wikipedia.org/wiki/"

    def search_article(self, topic: str) -> dict:
        """
        Busca un artículo en Wikipedia y obtiene su título
        y los primeros cinco párrafos.
        """

        topic_formatted = topic.strip().replace(" ", "_")

        url = self.BASE_URL + topic_formatted

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise Exception(
                f"No se pudo encontrar el artículo: {topic}"
            )

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1")

        if title is None:
            raise Exception("No se pudo encontrar el título del artículo.")

        paragraphs = soup.find_all("p")

        content = []

        for paragraph in paragraphs:
            text = paragraph.get_text(strip=True)

            if text:
                content.append(text)

            if len(content) == 5:
                break

        if len(content) < 5:
            raise Exception(
                "El artículo no contiene cinco párrafos disponibles."
            )

        return {
            "title": title.get_text(strip=True),
            "paragraphs": content
        }