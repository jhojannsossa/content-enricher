import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


class FileService:
    """Servicio encargado de guardar los documentos."""

    def __init__(self):
        self.output_directory = "output"

        os.makedirs(
            self.output_directory,
            exist_ok=True
        )

        # Fuentes Arial de Windows.
        self.font_regular = "Arial"
        self.font_bold = "Arial-Bold"

        arial_path = r"C:\Windows\Fonts\arial.ttf"
        arial_bold_path = r"C:\Windows\Fonts\arialbd.ttf"

        if os.path.exists(arial_path):
            pdfmetrics.registerFont(
                TTFont(
                    self.font_regular,
                    arial_path
                )
            )

        if os.path.exists(arial_bold_path):
            pdfmetrics.registerFont(
                TTFont(
                    self.font_bold,
                    arial_bold_path
                )
            )

    def save_txt(
        self,
        filename: str,
        title: str,
        original: str,
        enriched: str,
        translated: str
    ) -> str:

        if not filename.endswith(".txt"):
            filename += ".txt"

        filepath = os.path.join(
            self.output_directory,
            filename
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            file.write("=" * 60 + "\n")
            file.write("CONTENT ENRICHER\n")
            file.write("=" * 60 + "\n\n")

            file.write(f"TEMA: {title}\n\n")

            file.write("CONTENIDO ORIGINAL\n")
            file.write("-" * 60 + "\n")
            file.write(original)
            file.write("\n\n")

            file.write("CONTENIDO ENRIQUECIDO\n")
            file.write("-" * 60 + "\n")
            file.write(enriched)
            file.write("\n\n")

            file.write("CONTENIDO TRADUCIDO\n")
            file.write("-" * 60 + "\n")
            file.write(translated)

        return filepath

    def save_pdf(
        self,
        filename: str,
        title: str,
        original: str,
        enriched: str,
        translated: str
    ) -> str:

        if not filename.endswith(".pdf"):
            filename += ".pdf"

        filepath = os.path.join(
            self.output_directory,
            filename
        )

        pdf = canvas.Canvas(
            filepath,
            pagesize=A4
        )

        width, height = A4

        x = 50
        y = height - 50

        # Título principal
        pdf.setFont(
            self.font_bold,
            16
        )

        pdf.drawString(
            x,
            y,
            "CONTENT ENRICHER"
        )

        y -= 30

        sections = [
            ("TEMA", title),
            ("CONTENIDO ORIGINAL", original),
            ("CONTENIDO ENRIQUECIDO", enriched),
            ("CONTENIDO TRADUCIDO", translated)
        ]

        for section_title, content in sections:

            # Comprobar si queda espacio para el título.
            if y < 70:
                pdf.showPage()
                y = height - 50

            pdf.setFont(
                self.font_bold,
                12
            )

            pdf.drawString(
                x,
                y,
                section_title
            )

            y -= 20

            pdf.setFont(
                self.font_regular,
                9
            )

            # Procesar el contenido respetando los saltos de línea.
            paragraphs = content.split("\n")

            for paragraph in paragraphs:

                # Línea vacía.
                if not paragraph.strip():
                    y -= 10
                    continue

                words = paragraph.split()
                line = ""

                for word in words:

                    test_line = (
                        line + " " + word
                    ).strip()

                    if len(test_line) > 95:

                        if y < 50:
                            pdf.showPage()
                            y = height - 50

                            pdf.setFont(
                                self.font_regular,
                                9
                            )

                        pdf.drawString(
                            x,
                            y,
                            line
                        )

                        y -= 13

                        line = word

                    else:
                        line = test_line

                if line:

                    if y < 50:
                        pdf.showPage()
                        y = height - 50

                        pdf.setFont(
                            self.font_regular,
                            9
                        )

                    pdf.drawString(
                        x,
                        y,
                        line
                    )

                    y -= 13

            y -= 15

        pdf.save()

        return filepath