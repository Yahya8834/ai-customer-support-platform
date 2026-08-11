import pymupdf



class PdfTextExtractionService:

    @staticmethod
    def execute(file_path: str) -> str:
        """
        Extract all text from a PDF file.
        """
        document = pymupdf.open(file_path)

        try:
            extracted_text = ""

            for page in document:
                extracted_text += page.get_text()

            return extracted_text

        finally:
            document.close()