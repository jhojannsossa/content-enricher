from models.content import Content
from services.wikipedia_service import WikipediaService
from services.gemini_service import GeminiService
from services.translation_service import TranslationService
from services.file_service import FileService
from utils.validators import (
    validate_topic,
    validate_language,
    validate_filename
)


def print_separator():
    print("\n" + "=" * 70 + "\n")


def show_original_content(content: Content):
    print_separator()

    print("RESULTADO DE WIKIPEDIA")
    print("=" * 70)

    print(f"\nTítulo: {content.title}\n")

    print(content.original)


def show_enriched_content(enriched: str):
    print_separator()

    print("CONTENIDO ENRIQUECIDO CON GEMINI")
    print("=" * 70)

    print(enriched)


def show_translated_content(translated: str):
    print_separator()

    print("CONTENIDO TRADUCIDO")
    print("=" * 70)

    print(translated)


def ask_save_option() -> str:
    print_separator()

    print("¿Quieres guardar el contenido?")
    print("1. Sí")
    print("2. No")

    return input("\nSelecciona una opción: ").strip()


def save_content(
    content: Content,
    file_service: FileService
):
    print_separator()

    print("FORMATO DE GUARDADO")
    print("1. TXT")
    print("2. PDF")

    format_option = input(
        "\nSelecciona el formato: "
    ).strip()

    filename = input(
        "Introduce el nombre del archivo: "
    ).strip()

    if not validate_filename(filename):
        print("El nombre del archivo no es válido.")
        return

    if format_option == "1":

        saved_file = file_service.save_txt(
            filename,
            content.title,
            content.original,
            content.enriched,
            content.translated
        )

        print(
            f"\nArchivo guardado correctamente: "
            f"{saved_file}"
        )

    elif format_option == "2":

        saved_file = file_service.save_pdf(
            filename,
            content.title,
            content.original,
            content.enriched,
            content.translated
        )

        print(
            f"\nArchivo guardado correctamente: "
            f"{saved_file}"
        )

    else:
        print("\nFormato no válido.")


def main():

    print("=" * 70)
    print("                    CONTENT ENRICHER")
    print("=" * 70)

    topic = input(
        "\nIntroduce el tema que quieres investigar: "
    ).strip()

    if not validate_topic(topic):
        print("El tema no puede estar vacío.")
        return

    language = input(
        "Introduce el idioma de traducción "
        "(ejemplo: es, en, fr, de): "
    ).strip()

    if not validate_language(language):
        print("El idioma no puede estar vacío.")
        return

    try:

        # ------------------------------------------------
        # 1. WIKIPEDIA
        # ------------------------------------------------

        print("\nBuscando información en Wikipedia...")

        wikipedia_service = WikipediaService()

        content = wikipedia_service.search(topic)

        show_original_content(content)

        input(
            "\nPulsa ENTER para continuar..."
        )

        # ------------------------------------------------
        # 2. GEMINI
        # ------------------------------------------------

        print("\nEnriqueciendo contenido con Gemini...")

        gemini_service = GeminiService()

        enriched = gemini_service.enrich(
            content.title,
            content.original
        )

        content.enriched = enriched

        show_enriched_content(
            content.enriched
        )

        input(
            "\nPulsa ENTER para continuar..."
        )

        # ------------------------------------------------
        # 3. TRADUCCIÓN
        # ------------------------------------------------

        print(
            f"\nTraduciendo contenido al idioma: "
            f"{language}"
        )

        translation_service = TranslationService()

        translated = translation_service.translate(
            content.enriched,
            language
        )

        content.translated = translated

        show_translated_content(
            content.translated
        )

        input(
            "\nPulsa ENTER para continuar..."
        )

        # ------------------------------------------------
        # 4. GUARDAR
        # ------------------------------------------------

        save_option = ask_save_option()

        if save_option == "1":

            file_service = FileService()

            save_content(
                content,
                file_service
            )

        elif save_option == "2":

            print("\nNo se guardará ningún archivo.")

        else:

            print("\nOpción no válida.")

    except Exception as error:

        print_separator()

        print("SE HA PRODUCIDO UN ERROR")
        print("=" * 70)

        print(error)


if __name__ == "__main__":
    main()
