from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


class FileService:
    """Servicio encargado de guardar los documentos."""

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

        with open(
            filename,
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

        return filename

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

        pdf = canvas.Canvas(
            filename,
            pagesize=A4
        )

        width, height = A4

        x = 50
        y = height - 50

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(
            x,
            y,
            "CONTENT ENRICHER"
        )

        y -= 30

        pdf.setFont("Helvetica", 11)

        sections = [
            ("TEMA", title),
            ("CONTENIDO ORIGINAL", original),
            ("CONTENIDO ENRIQUECIDO", enriched),
            ("CONTENIDO TRADUCIDO", translated)
        ]

        for section_title, content in sections:

            if y < 70:
                pdf.showPage()
                y = height - 50
                pdf.setFont("Helvetica", 11)

            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(
                x,
                y,
                section_title
            )

            y -= 20

            pdf.setFont("Helvetica", 9)

            words = content.split()
            line = ""

            for word in words:

                test_line = (
                    line + " " + word
                ).strip()

                if len(test_line) > 95:

                    if y < 50:
                        pdf.showPage()
                        y = height - 50

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
                pdf.drawString(
                    x,
                    y,
                    line
                )
                y -= 20

            y -= 15

        pdf.save()

        return filename