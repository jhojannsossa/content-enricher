from services.wikipedia_service import WikipediaService


def main():
    print("=" * 50)
    print("       CONTENT ENRICHER")
    print("=" * 50)

    topic = input("\nIntroduce el tema que quieres investigar: ")

    wikipedia_service = WikipediaService()

    try:
        article = wikipedia_service.search_article(topic)

        print("\n" + "=" * 50)
        print("RESULTADO DE WIKIPEDIA")
        print("=" * 50)

        print(f"\nTítulo: {article['title']}\n")

        for index, paragraph in enumerate(article["paragraphs"], start=1):
            print(f"Párrafo {index}:")
            print(paragraph)
            print()

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()