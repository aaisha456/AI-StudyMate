from pypdf import PdfReader


def extract_text_from_pdf(file_path):
    """
    Extract text from all pages of a PDF.
    """

    try:

        reader = PdfReader(file_path)

        extracted_pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            try:

                text = page.extract_text()

                if text and text.strip():

                    extracted_pages.append(
                        f"--- Page {page_number} ---\n"
                        f"{text.strip()}"
                    )

            except Exception as page_error:

                print(
                    f"Error reading page {page_number}: "
                    f"{page_error}"
                )

        extracted_text = "\n\n".join(
            extracted_pages
        )

        return extracted_text.strip()


    except Exception as error:

        print(
            f"PDF extraction error: {error}"
        )

        return ""